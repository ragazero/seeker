from fastapi import APIRouter

router = APIRouter()

@router.get("/stream-url")
async def stream_url(track_id: str):
    return {"url": f"https://yourcdn.com/stream/{track_id}"}
