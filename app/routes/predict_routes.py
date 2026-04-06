from fastapi import APIRouter, UploadFile, File
import shutil

from app.ml.predictor import predict_ulcer
from app.services.report_service import create_ulcer_report
from app.schemas.report_schema import UlcerReportCreate  # IMPORTANT

router = APIRouter()


@router.post("/predict-ulcer")
async def predict_ulcer_api(
    file: UploadFile = File(...),
    patient_id: int = None,
    doctor_id: int = None,
    hospital_id: int = None
):

    # 📁 Save uploaded file
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🧠 Step 1: Run ML Prediction
    result = predict_ulcer(file_path)

    # 🧾 Step 2: Create Report Object (THIS MATCHES YOUR SERVICE)
    if patient_id and doctor_id and hospital_id:

        report_data = UlcerReportCreate(
            hospital_id=hospital_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            image_url=file_path,
            prediction_result=result["prediction"],
            confidence_score=result["confidence"],
            severity_level=result["prediction"],
            notes=None
        )

        report_id = create_ulcer_report(report_data)

        return {
            "message": "Prediction + Report Saved",
            "report_id": report_id,
            "result": result
        }

    # If no IDs provided → only prediction
    return result