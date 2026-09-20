import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class RetrievalService:
    def __init__(self):
        self.embed_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.chroma_client = chromadb.PersistentClient(path=settings.VECTOR_STORE_PATH)
        self.collection = self.chroma_client.get_or_create_collection(
            name="rag_knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )

    def retrieve(self, query: str, top_k: int = None) -> tuple[list[str], list[str]]:
        k = top_k or settings.TOP_K
        query_vector = self.embed_model.encode([query]).tolist()
        
        results = self.collection.query(
            query_embeddings=query_vector,
            n_results=k
        )
        
        contexts = []
        citations = []
        
        retrieved_docs = results["documents"][0]
        retrieved_metas = results["metadatas"][0]
        
        for doc, meta in zip(retrieved_docs, retrieved_metas):
            contexts.append(doc)
            citations.append(f"{meta['source']} (Page {meta['page']})")
            
        return contexts, list(dict.fromkeys(citations))