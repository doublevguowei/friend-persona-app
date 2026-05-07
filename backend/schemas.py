from pydantic import BaseModel, Field


class VoteCreate(BaseModel):
    voter_id: int = Field(..., ge=1)
    question_id: int = Field(..., ge=1)
    target_id: int = Field(..., ge=1)
