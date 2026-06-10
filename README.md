# AI-Powered Learning & Development Platform

This repository contains the Phase 0 foundation of an enterprise-grade Learning & Development SaaS platform.

It pairs an async FastAPI backend with a React/Vite frontend and a provider-agnostic AI orchestration layer built around LangGraph.

## Project Overview

This platform is designed to support AI-driven instructional design workflows for corporate learning programs, including:

- **Needs analysis** and learner profiling
- **Curriculum design** and module mapping
- **Storyboard and training content generation**
- **Review and quality assurance** of generated learning assets
- **Multi-tenant project management** for organizations and users

The backend is architected to be modular and extensible, with clearly separated API, service, workflow, and provider layers.

## Architecture Summary

### Backend (`app/`)

- **FastAPI API layer**: routes in `app/api/` expose authentication, project CRUD, AI endpoints, uploads, workflow control, and health checks.
- **Core services**: `app/services/` contains business logic and domain workflows for auth, projects, AI orchestration, uploads, and workflow state.
- **AI orchestration**: `app/workflows/` uses LangGraph state graphs for analysis, design, development, and review phases.
- **Agent layer**: `app/agents/` wraps workflow phases into reusable AI agent behaviors.
- **Provider-agnostic AI layer**: `app/providers/` centralizes LLM access, currently supporting Gemini and Ollama with fallback behavior.
- **Vector store**: `app/vectorstore/` manages ChromaDB embeddings, retrieval, and document ingestion.
- **Database and tenancy**: `app/db/`, `app/models/`, and `app/schemas/` define the ORM models, Pydantic schemas, and multi-tenant access patterns.
- **Background tasks**: `app/tasks/` provides async task orchestration using Celery for long-running AI workflows, ingestion, and export.
- **Middleware**: request logging, tenant enforcement, and auth middleware live in `app/middleware/`.

### Frontend (`content-studio-ui/`)

- Built with **React** and **Vite**
- Uses **Tailwind CSS** for styling
- Includes UI components for project and phase workflows, dashboards, and user interaction with AI-generated assets

## Key Capabilities

- **Tenant-aware project security** via `X-Organization-ID` headers
- **AI workflow orchestration** using LangGraph state graphs
- **Provider fallback** from Gemini to local Ollama when quota or availability fails
- **Structured model output** using Pydantic response schemas
- **ChromaDB-powered retrieval** for document context and prompt augmentation
- **Upload pipeline** for project files and storage integration

## How the Project Works

The platform is built as a staged ADDIE workflow pipeline. Each major step is a separate phase with its own dedicated API endpoints, persistence, and structured AI output.

1. **Project setup and needs analysis**
   - The user creates a learning project and provides organization, learner, and business context.
   - `app/api/analysis.py` exposes the analysis endpoint.
   - `app/services/ai_service.py` and `app/workflows/analysis_graph.py` generate structured learner profiles, gap analysis, and recommendations.
   - This phase stores output in `app/models/training_content.py` and can enrich prompts with document context from `app/vectorstore/retriever.py`.

2. **Curriculum design and module planning**
   - The platform converts the validated analysis output into a curriculum architecture.
   - `app/api/design.py` and `app/workflows/design_graph.py` orchestrate the design phase.
   - The design step uses `app/nodes/design_nodes.py` for explicit instruction-to-structure translation.

3. **Content development**
   - `app/api/development.py` triggers the content development phase only after design is complete.
   - `app/workflows/develop_graph.py` and `app/nodes/development_nodes.py` generate module-level content, submodule detail, and training narrative.

4. **Review and QA**
   - `app/api/review.py` runs the final review phase after development.
   - `app/workflows/review_graph.py` and `app/nodes/review_nodes.py` validate the content using structured review schemas.
   - Approved review output becomes the canonical export source for PDF, DOCX, and PPTX.

5. **Provider execution and fallback**
   - The AI layer chooses a provider in `app/providers/__init__.py`.
   - `app/providers/gemini_provider.py` is the primary cloud model path.
   - If Gemini hits quota or rate limits, the system can fallback to `app/providers/ollama_provider.py` for local Ollama generation.

6. **Persistence and retrieval**
   - Project, user, and workflow metadata persist in the database via `app/db/` and `app/models/`.
   - Phase outputs are stored in `app/models/training_content.py`.
   - Context vectors and embeddings are served from ChromaDB through `app/vectorstore/retriever.py`.

## Folder Structure

```text
app/
  api/
  core/
  db/
  middleware/
  models/
  providers/
  schemas/
  services/
  workflows/
  agents/
  vectorstore/
  tasks/
  websocket/
content-studio-ui/
  src/
  public/
  package.json
requirements.txt
README.md
project_structure.md
```

### Notable backend files

- `app/api/ai.py` — AI endpoint entry points for objectives, interactivity, storyboard, and needs analysis
- `app/core/config.py` — environment settings, provider options, and model configuration
- `app/providers/gemini_provider.py` — Gemini text/structured generation with Ollama fallback
- `app/providers/ollama_provider.py` — local Ollama CLI integration for offline or quota-safe generation
- `app/workflows/*.py` — LangGraph workflow graphs for each AI phase
- `app/vectorstore/retriever.py` — retrieves relevant context from ChromaDB

## Getting Started

1. Create a Python environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables in a `.env` file.

3. Run the backend:

```bash
uvicorn app.main:app --reload
```

4. Start the frontend:

```bash
cd content-studio-ui
npm install
npm run dev
```

## Local Ollama Support

The platform supports local Ollama access via `OLLAMA_MODEL` and `OLLAMA_BINARY_PATH` configuration. This provides a fallback path when Gemini quota is exhausted.

## Notes

- This repo is currently at a foundational Phase 0 stage and is intended as a clean, extensible starting point for enterprise AI-enabled learning platforms.
- The current AI stack is built to be provider-agnostic, so new model providers can be added under `app/providers/`.
- The frontend is a lightweight studio UI meant to connect to the backend API and visualize workflow phases.

---

If you need the README to include command examples for specific endpoints or a developer onboarding checklist, I can expand it further.