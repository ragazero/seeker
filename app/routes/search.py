from fastapi import APIRouter

router = APIRouter()

@router.get("/search")
async def search(q: str):
    return {"results": f"Searching for '{q}'..."}
