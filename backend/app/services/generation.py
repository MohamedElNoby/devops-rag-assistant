import ollama
from app.core.config import settings

class GenerationService:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_BASE_URL)

    def generate_grounded_answer(self, query: str, contexts: list[str]) -> str:
        combined_context = "\n\n".join(contexts)
        
        prompt = f"""You are a precise technical documentation assistant.
Answer the question accurately using the information provided in the context below.
Be concise and factual. If the context truly does not contain relevant details to answer the question, reply with: "The provided documentation does not contain enough information to answer this question."

Context:
{combined_context}

User Question:
{query}

Answer:"""

        response = self.client.generate(
            model=settings.OLLAMA_MODEL,
            prompt=prompt,
            options={"temperature": settings.TEMPERATURE}
        )
        
        return response["response"].strip()