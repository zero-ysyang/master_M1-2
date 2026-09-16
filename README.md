# 📊 Data-Aware AI Assistant (내 상황을 아는 AI 비서)

시계열 데이터를 기반으로 사용자의 상태를 파악하고 맞춤형 대화를 제공하는 웹 서비스입니다.

## 🔗 서비스 링크
- **Frontend (Vercel) :** https://master-m1-2-7ogs504yy-zero-ysyangs-projects.vercel.app
- **Backend API (Render) :** https://ai-service-backend-uno2.onrender.com
- **API Documentation :** https://ai-service-backend-uno2.onrender.com/docs

---

## 🛠️ 기술 스택 (Tech Stack)

### Frontend
- HTML5 / CSS3 / Vanilla JavaScript (ES6+)
- **Chart.js**: 데이터 시각화 차트 구현

### Backend
- **Python 3.11** / **FastAPI**: RESTful API 구현 및 Async 처리
- **Uvicorn**: ASGI 서버

### Database & AI Model
- **Google Cloud Firestore**: NoSQL 기반 사용자 데이터 및 대화 내역 저장
- **Google Gemini API (`gemini-3.5-flash`)**: Context-Aware AI 대화 엔진

### Deployment & Infrastructure
- **Vercel**: 프론트엔드 정적 웹 호스팅
- **Render**: 백엔드 파이썬 애플리케이션 서비스 호스팅

---

## ✨ 핵심 기능

1. **시계열 데이터 CRUD & 요약**: 사용자의 일별 수치 데이터 입력, 삭제, 통계 분석(평균, 최대/최소, 추세)
2. **Context-Aware AI 대화**: DB에 입력된 최신 데이터를 Gemini 프롬프트 context로 주입하여 데이터 기반 맞춤형 답변 생성
3. **대화 히스토리 관리**: 멀티 세션 대화 저장, 이전 대화 불러오기, 새 대화 시작 기능
4. **시각화 & 데이터 내보내기**: Chart.js 기반 추세 그래프 지원, UTF-8 BOM 지원 CSV 내보내기
5. **다크 모드 지원**: 사용자 편의를 위한 테마 토글

---

## 🚀 로컬 실행 방법

```bash
# 레포지토리 클론
git clone [https://github.com/your-username/your-repo.git](https://github.com/your-username/your-repo.git)
cd your-repo

# 가상환경 생성 및 패키지 설치
python -m venv venv
pip install -r requirements.txt

# 환경 변수(.env) 설정
# GEMINI_API_KEY, FIREBASE_CREDENTIALS_PATH, ALLOWED_ORIGINS 작성

# 서버 실행
uvicorn main:app --reload --port 8000
