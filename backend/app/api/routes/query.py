from fastapi import APIRouter, Request, HTTPException
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "DevOps RAG Backend"}

@router.post("/query", response_model=QueryResponse, tags=["RAG"])
async def handle_query(payload: QueryRequest, request: Request):
    try:
        retrieval_service = request.app.state.retrieval_service
        generation_service = request.app.state.generation_service
        
        contexts, sources = retrieval_service.retrieve(payload.question)
        answer = generation_service.generate_grounded_answer(payload.question, contexts)
        
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))