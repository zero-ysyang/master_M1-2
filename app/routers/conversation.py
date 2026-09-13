from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import ConversationCreate, ConversationResponse
from app.services import chat_service

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def save_conv(payload: ConversationCreate):
    conv_id = chat_service.save_conversation(payload.messages, title=payload.title)
    return {"id": conv_id, "message": "대화가 성공적으로 저장되었습니다."}

@router.get("", response_model=List[ConversationResponse])
def list_convs():
    return chat_service.get_conversations()

@router.get("/{conv_id}", response_model=ConversationResponse)
def get_single_conv(conv_id: str):
    conv = chat_service.get_conversation_by_id(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="대화 기록을 찾을 수 없습니다.")
    return conv

@router.delete("/{conv_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conv(conv_id: str):
    success = chat_service.delete_conversation(conv_id)
    if not success:
        raise HTTPException(status_code=404, detail="대화 기록을 찾을 수 없습니다.")