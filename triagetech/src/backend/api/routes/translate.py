from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def translate_text(data: dict):
    return {"translated_text": "नमस्ते"}
