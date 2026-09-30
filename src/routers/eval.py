from fastapi import APIRouter, FastAPI
router = APIRouter() 

@router.get("/eval")
async def eval():
    return {"message": "This is eval endpoint"}