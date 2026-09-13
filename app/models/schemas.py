from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- 1. 시계열 데이터 스키마 ---
class DataCreate(BaseModel):
    date: str = Field(..., example="2025-01-15", description="날짜 (YYYY-MM-DD)")
    value: float = Field(..., example=5.5, description="수치 데이터")
    memo: Optional[str] = Field(None, example="FastAPI 연동 완료", description="메모")

class DataUpdate(BaseModel):
    date: Optional[str] = Field(None, example="2025-01-15")
    value: Optional[float] = Field(None, example=6.0)
    memo: Optional[str] = Field(None, example="수정된 메모")

class DataResponse(DataCreate):
    id: str = Field(..., description="Firestore 문서 ID")

# --- 2. 데이터 요약 스키마 ---
class Metrics(BaseModel):
    total: float
    average: float
    max: float
    min: float

class DataSummary(BaseModel):
    period: str
    count: int
    metrics: Metrics
    trend: str

# --- 3. 대화 및 AI 챗봇 스키마 ---
class ChatMessage(BaseModel):
    role: str = Field(..., example="user", description="user 또는 assistant")
    content: str = Field(..., example="이번 달 학습 시간 평균이 어때?")

class ChatRequest(BaseModel):
    message: str = Field(..., example="최근 데이터 트렌드 알려줘.")
    conversation_id: Optional[str] = Field(None, description="기존 대화에 이어하기 위한 ID")

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    summary_used: DataSummary

class ConversationCreate(BaseModel):
    title: Optional[str] = "새 대화"
    messages: List[ChatMessage]

class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    messages: Optional[List[ChatMessage]] = None