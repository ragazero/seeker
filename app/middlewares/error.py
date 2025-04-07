from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

def add_error_handling(app: FastAPI):
    @app.middleware("http")
    async def error_handling_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logging.exception("Unhandled exception occurred")
            return JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred"},
            )
