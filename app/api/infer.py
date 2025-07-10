from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ollama_wrapper import OllamaLLM

router = APIRouter()
llm = OllamaLLM()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/infer")
def infer(prompt_request: PromptRequest):
    response = llm.generate_answer(prompt_request.prompt)
    return {"response": response}
