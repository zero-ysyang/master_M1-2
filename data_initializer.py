import os
import random
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Firebase 초기화
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 100개의 시계열 샘플 데이터 생성 (최근 100일간 학습 시간 기록 예시)
def generate_sample_data():
    data_list = []
    base_date = datetime.now() - timedelta(days=100)
    
    memos = ["파이썬 기초 공부", "FastAPI 라우터 설계", "Firestore 데이터베이스 연동", "AI 프롬프트 엔지니어링", "프론트엔드 CSS 수정", "휴식 및 복습"]
    
    for i in range(100):
        current_date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        value = round(random.uniform(1.5, 8.0), 1)  # 1.5 ~ 8.0 시간
        memo = random.choice(memos)
        
        data_list.append({
            "date": current_date,
            "value": value,
            "memo": memo
        })
    return data_list

def upload_to_firestore():
    sample_data = generate_sample_data()
    collection_ref = db.collection("data")
    
    print("Firestore에 데이터 업로드 중...")
    for item in sample_data:
        collection_ref.add(item)
    print(f"성공적으로 {len(sample_data)}개의 데이터를 Firestore 'data' 컬렉션에 추가했습니다.")

if __name__ == "__main__":
    upload_to_firestore()