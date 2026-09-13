from pydantic import BaseModel, Field
from typing import List


class AskRequest(BaseModel):
    question: str = Field(..., description="The user's natural language question")
    top_k: int = Field(
        default=3, ge=1, le=10, description="Number of context chunks to retrieve"
    )


class SourceItem(BaseModel):
    source: str
    similarity: float


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
