import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.utils.logger import logger
from fastapi.responses import FileResponse
import os

app = FastAPI(title="KB Assistant API", description="Enterprise RAG Application")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

os.makedirs("frontend", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/docs", StaticFiles(directory="data/documents"), name="docs")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Unable to process request. Please try again."}
    )
