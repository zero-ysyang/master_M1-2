from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.schemas import DataCreate, DataUpdate, DataResponse, DataSummary
from app.services import data_service

router = APIRouter()

@router.post("", response_model=DataResponse, status_code=status.HTTP_201_CREATED)
def create_new_data(payload: DataCreate):
    return data_service.create_data(payload)

@router.get("", response_model=List[DataResponse])
def read_data_list():
    return data_service.get_all_data()

@router.get("/summary", response_model=DataSummary)
def read_data_summary():
    return data_service.calculate_summary()

@router.put("/{doc_id}", response_model=DataResponse)
def update_existing_data(doc_id: str, payload: DataUpdate):
    result = data_service.update_data(doc_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail="해당 데이터를 찾을 수 없습니다.")
    return result

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_data(doc_id: str):
    success = data_service.delete_data(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="해당 데이터를 찾을 수 없습니다.")