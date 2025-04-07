from fastapi import APIRouter, Query, HTTPException
import logging
from typing import Optional
from ytmusicapi import YTMusic

yt = YTMusic()
router = APIRouter()

PLATFORM = "ytmusic"
VALID_FILTERS = {"songs", "videos", "albums", "artists", "playlists"}

@router.get("/search")
async def search(
    q: str = Query(..., description="Search query"),
    filter: Optional[str] = Query("songs", description="Filter for search results"),
    limit: Optional[int] = Query(10, description="Number of results to return", ge=1, le=50)
):
    if filter not in VALID_FILTERS:
        raise HTTPException(status_code=400, detail=f"Invalid filter '{filter}'. Allowed filters: {', '.join(VALID_FILTERS)}")

    try:
        results = yt.search(q, filter=filter, limit=limit)

        tracks = []
        for item in results:
            if "videoId" not in item:
                continue

            track = {
                "content_id": item["videoId"],
                "platform": PLATFORM,
                "title": item["title"],
                "artists": item.get("artists", []),
                "album": item.get("album", {}),
                "duration_ms": item.get("duration_seconds", 0) * 1000,
                "explicit": item.get("isExplicit", False),
                "images": item.get("thumbnails", []),
                "category": item["category"],
                "result_type": item["resultType"],
            }
            tracks.append(track)

        return {"tracks": tracks[:limit]}

    except Exception as e:
        logging.error(f"Error in search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")
