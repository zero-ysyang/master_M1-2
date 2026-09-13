import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

# 이미 초기화된 경우 재초기화 방지
if not firebase_admin._apps:
    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    
    # Render 등 배포 환경에서 환경 변수에 JSON 문자열이 통째로 들어올 경우를 대비한 로직 포함
    firebase_json_env = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    
    if firebase_json_env:
        cred_dict = json.loads(firebase_json_env)
        cred = credentials.Certificate(cred_dict)
    elif os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
    else:
        raise FileNotFoundError(f"Firebase 키 파일을 찾을 수 없습니다: {cred_path}")

    firebase_admin.initialize_app(cred)

db = firestore.client()