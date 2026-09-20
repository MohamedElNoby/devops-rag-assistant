from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, description="The user query to be answered from documentation")

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]