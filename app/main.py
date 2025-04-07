from fastapi import FastAPI
from app.routes import search, stream
from app.middlewares.error import add_error_handling
from app.logger import setup_logging

app = FastAPI()

setup_logging()
add_error_handling(app)

@app.get("/ping")
def ping():
    return {"message": "pong"}

API_PREFIX = "/api/v1"
app.include_router(search.router, prefix=API_PREFIX)
app.include_router(stream.router, prefix=API_PREFIX)
