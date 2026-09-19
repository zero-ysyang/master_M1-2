# 📊 학습시간 트렌드 AI 비서

시계열 데이터를 기반으로 맞춤형 대화를 제공하는 웹 서비스입니다.

## 🔗 서비스 링크
- **Frontend (Vercel) :** https://master-m1-2.vercel.app
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
git clone https://github.com/zero-ysyang/master_M1-2.git

# 가상환경 생성 및 패키지 설치
python -m venv venv
pip install -r requirements.txt

# 환경 변수(.env) 설정
GEMINI_API_KEY, FIREBASE_CREDENTIALS_PATH, ALLOWED_ORIGINS 작성

# 서버 실행
uvicorn main:app --reload --port 8000
```

---

## 📌 스크린샷

### 1) 데이터 요약이 보이는 채팅 화면 (질문+답변 포함)
<img width="1015" height="941" alt="11" src="https://github.com/user-attachments/assets/af40813c-2c82-4938-9a6d-0239fd56e037" />


### 2) 데이터 관리 화면 (데이터 추가)
<img width="970" height="887" alt="22" src="https://github.com/user-attachments/assets/fecf73ea-ed65-438b-bb84-97a745163de3" />
<p></p>
<img width="956" height="898" alt="33" src="https://github.com/user-attachments/assets/914ce335-3a93-43c9-85a9-093149a38b36" />  


### 3) 대화 기록 화면 (불러오기 동작)
<img width="946" height="608" alt="44" src="https://github.com/user-attachments/assets/910eaac5-d8f8-43d6-95ea-59948da585fd" />



