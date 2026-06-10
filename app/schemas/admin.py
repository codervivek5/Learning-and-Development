from pydantic import BaseModel

class AdminResponse(BaseModel):
    id: int
    role: str
    email: str
    full_name: str
    is_active: bool
