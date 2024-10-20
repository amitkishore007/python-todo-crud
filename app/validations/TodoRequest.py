from pydantic import BaseModel, Field #type: ignore

class TodoRequest(BaseModel):
    title: str = Field(min_length=2, max_length=90)
    description: str = Field(min_length=2, max_length=255)
    is_active: bool
    rating: int = Field(gt=-1, lt=6)