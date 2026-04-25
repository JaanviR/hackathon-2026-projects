from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def triage_symptoms(data: dict):
    return {"severity": "LOW", "recommendation": "Rest at home"}
