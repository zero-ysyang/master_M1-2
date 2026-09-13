from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.firebase import db
from app.models.schemas import ChatMessage

CONV_COLLECTION = "conversations"

def save_conversation(messages: List[ChatMessage], conv_id: Optional[str] = None, title: Optional[str] = None) -> str:
    msg_dicts = [m.model_dump() for m in messages]
    
    if conv_id:
        doc_ref = db.collection(CONV_COLLECTION).document(conv_id)
        doc_ref.update({"messages": msg_dicts})
        return conv_id
    else:
        doc_ref = db.collection(CONV_COLLECTION).document()
        first_msg = messages[0].content if messages else "새 대화"
        conv_title = title if title else (first_msg[:20] + "...")
        doc_data = {
            "title": conv_title,
            "created_at": datetime.now().isoformat(),
            "messages": msg_dicts
        }
        doc_ref.set(doc_data)
        return doc_ref.id

def get_conversations() -> List[Dict[str, Any]]:
    docs = db.collection(CONV_COLLECTION).order_by("created_at", direction="DESCENDING").stream()
    result = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        result.append(item)
    return result

def get_conversation_by_id(conv_id: str) -> Optional[Dict[str, Any]]:
    doc = db.collection(CONV_COLLECTION).document(conv_id).get()
    if not doc.exists:
        return None
    item = doc.to_dict()
    item["id"] = doc.id
    return item

def delete_conversation(conv_id: str) -> bool:
    doc_ref = db.collection(CONV_COLLECTION).document(conv_id)
    if not doc_ref.get().exists:
        return False
    doc_ref.delete()
    return True