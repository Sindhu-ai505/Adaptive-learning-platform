from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def ai_status():
    return {
        "message": "AI API is working"
    }