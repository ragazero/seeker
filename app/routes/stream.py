from fastapi import APIRouter, Query, HTTPException
import logging
from urllib.parse import urlparse, parse_qs
import yt_dlp

router = APIRouter()

ydl_opts = {
    'format': 'bestaudio',
    'quiet': True,
    'noplaylist': True,
    'extract_flat': False,
}
ydl = yt_dlp.YoutubeDL(ydl_opts)

@router.get("/stream-url")
async def stream_url(
    videoId: str = Query(..., description="Video ID")
):
    try:
      info = ydl.extract_info(f"https://music.youtube.com/watch?v={videoId}", download=False)
      if not 'url' in info:
          raise HTTPException(status_code=404, detail="Stream URL not found")

      stream_url = info['url']

      parsed_url = urlparse(stream_url)
      query_params = parse_qs(parsed_url.query)
      expire_timestamp = query_params.get("expire", [None])[0]

      return {
          "url": stream_url,
          "expires_at": int(expire_timestamp) if expire_timestamp else None
      }

    except Exception as e:
        logging.error(f"Error fetching stream url: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error. Please try again later.")
