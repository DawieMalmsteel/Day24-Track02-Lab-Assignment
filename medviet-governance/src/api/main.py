# src/api/main.py
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
import pandas as pd

from src.access.rbac import get_current_user, require_permission
from src.pii.anonymizer import MedVietAnonymizer

app = FastAPI(title="MedViet Data API", version="1.0.0")
anonymizer = MedVietAnonymizer()
RAW_DATA_PATH = "data/raw/patients_raw.csv"


@app.get("/api/patients/raw")
@require_permission(resource="patient_data", action="read")
async def get_raw_patients(current_user: dict = Depends(get_current_user)):
    """Trả về raw patient data (chỉ admin được phép)."""
    df = pd.read_csv(RAW_DATA_PATH)
    return JSONResponse(content={"data": df.head(10).to_dict(orient="records")})


@app.get("/api/patients/anonymized")
@require_permission(resource="training_data", action="read")
async def get_anonymized_patients(current_user: dict = Depends(get_current_user)):
    """Trả về anonymized data (ml_engineer và admin được phép)."""
    df = pd.read_csv(RAW_DATA_PATH)
    df_anon = anonymizer.anonymize_dataframe(df)
    return JSONResponse(content={"data": df_anon.head(10).to_dict(orient="records")})


@app.get("/api/metrics/aggregated")
@require_permission(resource="aggregated_metrics", action="read")
async def get_aggregated_metrics(current_user: dict = Depends(get_current_user)):
    """Trả về aggregated metrics (không có PII)."""
    df = pd.read_csv(RAW_DATA_PATH)
    metrics = df.groupby("benh").size().reset_index(name="so_benh_nhan")
    return JSONResponse(content={"data": metrics.to_dict(orient="records")})


@app.delete("/api/patients/{patient_id}")
@require_permission(resource="patient_data", action="delete")
async def delete_patient(patient_id: str, current_user: dict = Depends(get_current_user)):
    """Chỉ admin được xóa (RBAC xử lý quyền)."""
    return {"message": f"Patient {patient_id} deleted (mock).", "deleted_by": current_user["username"]}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "MedViet Data API"}
