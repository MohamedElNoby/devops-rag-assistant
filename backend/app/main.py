from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.query import router as query_router
from app.services.retrieval import RetrievalService
from app.services.generation import GenerationService
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load vector store and services once at startup
    print("Loading vector store and embedding models into memory...")
    app.state.retrieval_service = RetrievalService()
    app.state.generation_service = GenerationService()
    print("Services initialized successfully.")
    yield
    print("Shutting down services...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)