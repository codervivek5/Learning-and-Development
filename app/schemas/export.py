from pydantic import BaseModel


class ExportResponse(BaseModel):
    project_id: int
    export_type: str
    filename: str
    status: str
    message: str
