# app/providers/ollama_provider.py
import asyncio
import json
import re
import shutil
from typing import Any, Dict, List, Optional, Pattern, Type, Union

from pydantic import BaseModel

from app.core.config import settings
from app.providers.base import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):
    """Local Ollama provider wrapper using the Ollama CLI."""

    ANSI_CSI_REGEX: Pattern[str] = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    CONTROL_CHAR_REGEX: Pattern[str] = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")

    def __init__(self) -> None:
        self.binary = settings.OLLAMA_BINARY_PATH or shutil.which("ollama")
        if not self.binary:
            raise ValueError(
                "Ollama binary not found. Set OLLAMA_BINARY_PATH or install ollama on PATH."
            )

        self.model = settings.OLLAMA_MODEL
        if not self.model:
            raise ValueError("OLLAMA_MODEL must be set for OllamaProvider.")

        self.temperature = settings.OLLAMA_TEMPERATURE

    async def _run_ollama(self, prompt: str, output_format: Optional[str] = None) -> str:
        cmd = [
            self.binary,
            "run",
            self.model,
            prompt,
            "--nowordwrap",
        ]
        if output_format:
            cmd.extend(["--format", output_format])

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(
                f"Ollama CLI failed: {stderr.decode().strip() or 'unknown error'}"
            )

        output = stdout.decode()
        output = self.ANSI_CSI_REGEX.sub("", output)
        output = self.CONTROL_CHAR_REGEX.sub("", output)
        return output.strip()

    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        if system_instruction:
            prompt = f"System: {system_instruction}\n\n{prompt}"

        return await self._run_ollama(prompt)

    async def generate_structured(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> BaseModel:
        if system_instruction:
            prompt = f"System: {system_instruction}\n\n{prompt}"

        prompt = (
            prompt
            + "\n\nRespond with valid JSON only. Do not include markdown, backticks, code fences, or any explanation."
        )

        text_response = await self._run_ollama(prompt, output_format="json")
        try:
            return response_schema.model_validate_json(text_response)
        except Exception as e:
            try:
                parsed = json.loads(text_response)
            except json.JSONDecodeError:
                raise RuntimeError(
                    f"Ollama structured output was not valid JSON: {str(e)}. Raw output: {text_response}"
                ) from e

            normalized = BaseLLMProvider._normalize_structured_payload(
                parsed, response_schema
            )
            try:
                return response_schema.model_validate(normalized)
            except Exception as e2:
                raise RuntimeError(
                    f"Ollama structured output was not valid JSON: {str(e2)}. Raw output: {text_response}"
                ) from e2

    async def generate_embeddings(
        self,
        texts: Union[str, List[str]],
    ) -> List[List[float]]:
        raise NotImplementedError(
            "OllamaProvider does not support embeddings. "
            "Set EMBEDDING_PROVIDER to a provider that supports embedding generation."
        )
