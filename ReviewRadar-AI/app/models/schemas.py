from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class ReviewResult(BaseModel):
    review_id: str
    product_id: str
    rating: str
    review_text: str
    similarity_score: float

class QueryResponse(BaseModel):
    query: str
    results: List[ReviewResult]
