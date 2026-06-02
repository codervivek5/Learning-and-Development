from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Utility schema to validate standard list pagination requests."""

    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=10, ge=1, le=100, description="Max number of items to return")
