from typing import List, Dict, Any, Optional
from app.core.firebase import db
from app.models.schemas import DataCreate, DataUpdate, DataSummary, Metrics

DATA_COLLECTION = "data"

def create_data(data: DataCreate) -> Dict[str, Any]:
    doc_ref = db.collection(DATA_COLLECTION).document()
    doc_data = data.model_dump()
    doc_ref.set(doc_data)
    return {"id": doc_ref.id, **doc_data}

def get_all_data() -> List[Dict[str, Any]]:
    docs = db.collection(DATA_COLLECTION).order_by("date").stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)
    return result

def update_data(doc_id: str, data: DataUpdate) -> Optional[Dict[str, Any]]:
    doc_ref = db.collection(DATA_COLLECTION).document(doc_id)
    if not doc_ref.get().exists:
        return None
    
    update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
    if update_dict:
        doc_ref.update(update_dict)
    
    updated_doc = doc_ref.get().to_dict()
    updated_doc["id"] = doc_id
    return updated_doc

def delete_data(doc_id: str) -> bool:
    doc_ref = db.collection(DATA_COLLECTION).document(doc_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True

def calculate_summary() -> DataSummary:
    items = get_all_data()
    if not items:
        return DataSummary(
            period="데이터 없음",
            count=0,
            metrics=Metrics(total=0, average=0, max=0, min=0),
            trend="데이터 부족"
        )

    values = [item["value"] for item in items]
    dates = [item["date"] for item in items]
    
    period_str = f"{min(dates)} ~ {max(dates)}"
    count = len(values)
    
    total_val = round(sum(values), 2)
    avg_val = round(total_val / count, 2)
    max_val = round(max(values), 2)
    min_val = round(min(values), 2)
    
    # 트렌드 연산 (최근 14개 vs 이전 14개 평균 비교)
    if count >= 28:
        recent_avg = sum(values[-14:]) / 14
        prev_avg = sum(values[-28:-14]) / 14
        diff = recent_avg - prev_avg
        if diff > 0.3:
            trend_str = f"상승 추세 (최근 평균: {round(recent_avg, 1)})"
        elif diff < -0.3:
            trend_str = f"하강 추세 (최근 평균: {round(recent_avg, 1)})"
        else:
            trend_str = "유지/보합 추세"
    else:
        trend_str = "데이터 누적 중"

    return DataSummary(
        period=period_str,
        count=count,
        metrics=Metrics(total=total_val, average=avg_val, max=max_val, min=min_val),
        trend=trend_str
    )