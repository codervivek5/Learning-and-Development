from pydantic import BaseModel
from typing import List


class DevelopedSubModule(BaseModel):
    title: str
    content: str


class DevelopedModule(BaseModel):
    title: str
    content: str
    submodules: List[DevelopedSubModule]


class DevelopmentResponse(BaseModel):
    modules: List[DevelopedModule]