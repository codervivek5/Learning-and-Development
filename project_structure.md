app/
│
├── api/
│   ├── auth.py               # JWT signup / login / refresh
│   ├── projects.py           # CRUD for Project entity
│   ├── uploads.py            # File upload endpoints
│   ├── ai.py                 # AI service endpoints (invoke LangGraph)
│   ├── workflow.py           # Trigger / monitor workflows
│   └── health.py            # /health‑check endpoint
│
├── core/
│   ├── config.py            # Pydantic Settings (reads .env)
│   ├── security.py          # Password hashing, JWT utilities
│   ├── logging.py           # Structured logging (jsonlog / loguru)
│   ├── database.py          # Async engine & SessionLocal factory
│   └── constants.py         # Global constants (e.g., roles, tenant keys)
│
├── db/
│   ├── session.py           # Async DB session helper
│   ├── base.py              # Base ORM class (includes TenantMixin)
│   └── migrations/          # Alembic migration scripts (auto‑generated)
│
├── models/
│   ├── user.py
│   ├── organization.py
│   ├── project.py
│   ├── workflow.py
│   └── document.py
│
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── project.py
│   ├── workflow.py
│   └── ai.py
│
├── services/
│   ├── auth_service.py
│   ├── project_service.py
│   ├── ai_service.py
│   ├── upload_service.py
│   └── workflow_service.py
│
├── providers/
│   ├── base.py               # Abstract BaseLLMProvider
│   ├── gemini_provider.py    # Gemini implementation
│   ├── openai_provider.py   # (stub) OpenAI implementation
│   └── claude_provider.py    # (stub) Claude implementation
│
├── workflows/
│   ├── analysis_graph.py
│   ├── design_graph.py
│   ├── develop_graph.py
│   └── review_graph.py
│
├── agents/
│   ├── analysis_agent.py
│   ├── curriculum_agent.py
│   ├── storyboard_agent.py
│   └── review_agent.py
│
├── prompts/
│   ├── analysis/
│   ├── design/
│   ├── develop/
│   └── review/
│
├── vectorstore/
│   ├── chroma_client.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── ingestion.py
│
├── tasks/
│   ├── embeddings_task.py
│   ├── export_task.py
│   ├── ingestion_task.py
│   └── ai_generation_task.py
│
├── middleware/
│   ├── auth_middleware.py
│   ├── logging_middleware.py
│   └── tenant_middleware.py
│
├── utils/
│   ├── fastapi_helpers.py
│   └── common.py
│
├── storage/
│   ├── uploads/            # runtime upload folder (mounted)
│   ├── generated/          # AI‑generated assets (images, PDFs)
│   └── temp/               # temporary processing files
│
└── websocket/
    └── ws_handler.py      # future WebSocket endpoint (e.g., live progress)
