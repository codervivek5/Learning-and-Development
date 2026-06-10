from pydantic import BaseModel


class ReviewResponse(BaseModel):
    score: int
    strengths: list[str]
    improvements: list[str]
    approved: bool