# models/ai_provider_config.py

class AIProviderConfig(Base):
    id
    organization_id

    provider_name
    model_name

    temperature
    max_tokens

    is_active

    created_at