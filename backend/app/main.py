import os
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure venv/Scripts and bundled ffmpeg are in PATH
scripts_dir = os.path.join(sys.prefix, 'Scripts')
if os.path.exists(scripts_dir) and scripts_dir not in os.environ.get('PATH', ''):
    os.environ['PATH'] = scripts_dir + os.pathsep + os.environ.get('PATH', '')

try:
    import imageio_ffmpeg
    ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    if os.path.exists(ffmpeg_dir) and ffmpeg_dir not in os.environ.get('PATH', ''):
        os.environ['PATH'] = ffmpeg_dir + os.pathsep + os.environ.get('PATH', '')
except Exception:
    pass

from app.database import engine, Base
from app.config import settings
from app.utils.exceptions import VideoSummarizerException

from app.routers import auth, summarize, quiz, notes, upload

app = FastAPI(title="Video Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.exception_handler(VideoSummarizerException)
async def video_summarizer_exception_handler(request: Request, exc: VideoSummarizerException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

app.include_router(auth.router)
app.include_router(summarize.router)
app.include_router(quiz.router)
app.include_router(notes.router)
app.include_router(upload.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Video Summarizer API"}
