from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, ReviewResult
from app.services.vector_store import vector_store

router = APIRouter()

@router.post("/search", response_model=QueryResponse)
async def semantic_search(request: QueryRequest):
    try:
        # Perform search in ChromaDB
        results = vector_store.search(request.query, request.top_k)
        
        review_results = []
        # ChromaDB returns lists of lists. Since we only have 1 query, we take index 0.
        if results and results["ids"] and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                # Compute similarity score from distance.
                # For cosine distance, similarity is 1 - distance
                distance = results["distances"][0][i] if results.get("distances") else 0
                similarity = 1.0 - distance
                
                metadata = results["metadatas"][0][i]
                document = results["documents"][0][i]
                
                review_result = ReviewResult(
                    review_id=str(metadata.get("review_id", "N/A")),
                    product_id=str(metadata.get("product_id", "N/A")),
                    rating=str(metadata.get("rating", "N/A")),
                    review_text=document,
                    similarity_score=round(similarity, 4)
                )
                review_results.append(review_result)
                
        return QueryResponse(query=request.query, results=review_results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during search: {str(e)}")
