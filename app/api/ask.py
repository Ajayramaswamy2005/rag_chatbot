from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.vector_store import search_across_collections
from app.services.ollama_wrapper import OllamaLLM

router = APIRouter()
llm = OllamaLLM()

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(req: AskRequest):
    results = search_across_collections(req.question, top_k=3)

    if not results:
        raise HTTPException(status_code=404, detail="No relevant context found in documents.")

    context = "\n".join([res["text"] for res in results])
    prompt = f"Use the context to answer the question.\n\nContext:\n{context}\n\nQuestion: {req.question}\nAnswer:"

    return {
        "response": llm.generate_answer(prompt)
    }
