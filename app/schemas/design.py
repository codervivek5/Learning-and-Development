from pydantic import BaseModel
from typing import List


class DesignSubModule(BaseModel):
    title: str
    description: str


class DesignModule(BaseModel):
    title: str
    description: str
    submodules: List[DesignSubModule]


class DesignResponse(BaseModel):
    course_title: str
    modules: List[DesignModule]