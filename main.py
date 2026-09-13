from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import data, chat, conversation
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="Data-Aware AI Assistant API",
    description="시계열 데이터 관리 및 데이터 맞춤형 AI 대화 서비스 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 통신 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API Server is running"}

# 라우터 등록
app.include_router(data.router, prefix="/api/data", tags=["Data"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat"])
app.include_router(conversation.router, prefix="/api/conversations", tags=["Conversations"])


if os.path.exists("frontend"):
    app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")