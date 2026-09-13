from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse, ChatMessage
from app.services import data_service, ai_service, chat_service

router = APIRouter()

@router.post("", response_model=ChatResponse)
def chat_with_ai(payload: ChatRequest):
    # 1. 현재 데이터 요약 획득
    summary = data_service.calculate_summary()
    
    # 2. 기존 대화 기록 로드 (이어하기일 경우)
    history_messages = []
    if payload.conversation_id:
        existing_conv = chat_service.get_conversation_by_id(payload.conversation_id)
        if existing_conv and "messages" in existing_conv:
            history_messages = existing_conv["messages"]

    # 3. Gemini AI 호출 (시스템 프롬프트 컨텍스트 주입)
    ai_reply = ai_service.generate_ai_response(payload.message, summary, history_messages)

    # 4. 대화 내역 업데이트 및 Firestore에 자동 저장
    new_messages = [ChatMessage(**m) for m in history_messages]
    new_messages.append(ChatMessage(role="user", content=payload.message))
    new_messages.append(ChatMessage(role="assistant", content=ai_reply))

    saved_id = chat_service.save_conversation(
        messages=new_messages, 
        conv_id=payload.conversation_id
    )

    return ChatResponse(
        conversation_id=saved_id,
        reply=ai_reply,
        summary_used=summary
    )