from google import genai
from google.genai import types
from app.core.config import settings
from app.models.schemas import DataSummary

# Gemini 클라이언트 초기화
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_ai_response(user_message: str, summary: DataSummary, history: list = None) -> str:
    try:
        # 1. 시스템 프롬프트 작성
        system_prompt = f"""
당신은 사용자의 데이터를 완벽히 이해하고 대화하는 데이터 전담 AI 비서입니다.
아래 제공된 [사용자 데이터 요약]을 참고하여 사용자의 질문에 친절하게 답변하세요.

[사용자 데이터 요약]
- 데이터 측정 기간: {summary.period}
- 총 기록 건수: {summary.count}개
- 주요 통계 지표:
  * 총합: {summary.metrics.total}
  * 평균: {summary.metrics.average}
  * 최댓값: {summary.metrics.max}
  * 최솟값: {summary.metrics.min}
- 최근 트렌드: {summary.trend}

답변 시 위 통계 수치를 자연스럽게 인용하세요.
"""

        # 2. 메시지 구성 (기존 대화 이력 포함)
        contents = []
        if history:
            for msg in history:
                # Firestore에서 가져온 dict 또는 Pydantic 객체 처리
                role = msg.get("role") if isinstance(msg, dict) else msg.role
                content = msg.get("content") if isinstance(msg, dict) else msg.content
                
                # Gemini SDK 역할 명칭 매핑 ("assistant" -> "model")
                genai_role = "model" if role in ["assistant", "model"] else "user"
                contents.append(
                    types.Content(
                        role=genai_role, 
                        parts=[types.Part.from_text(text=content)]
                    )
                )

        # 사용자 현재 메시지 추가
        contents.append(
            types.Content(
                role="user", 
                parts=[types.Part.from_text(text=user_message)]
            )
        )

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
            max_output_tokens=1000
        )

        # 3. Gemini 3.5 Flash 모델 호출
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=config
        )

        return response.text

    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return f"AI 응답 생성 중 오류가 발생했습니다: {str(e)}"