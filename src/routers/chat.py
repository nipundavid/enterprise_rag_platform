from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from ..generation import generate_answer
router = APIRouter() 

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat")
async def chat(chat_request: ChatRequest):
    return ChatResponse(response=generate_answer(chat_request.query))