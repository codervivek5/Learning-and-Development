from typing import List, Union
from app.providers import get_provider


async def get_embeddings(texts: Union[str, List[str]]) -> List[List[float]]:
    """Generate vector embeddings for text using the active LLM provider."""
    provider = get_provider()
    return await provider.generate_embeddings(texts)
