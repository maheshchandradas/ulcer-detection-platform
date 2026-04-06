from fastapi import APIRouter
from app.schemas.report_schema import UlcerReportCreate
from app.services.report_service import create_ulcer_report, get_patient_history

router = APIRouter()


# CREATE ULCER REPORT (Manual)
@router.post("/ulcer-report")
def add_ulcer_report(report: UlcerReportCreate):

    report_id = create_ulcer_report(report)

    return {
        "message": "Ulcer report created successfully",
        "report_id": report_id
    }


# GET PATIENT HISTORY (FINAL + GRAPH READY)
@router.get("/patient-history/{patient_id}")
def fetch_patient_history(patient_id: int):

    history = get_patient_history(patient_id)

    # Convert to graph-ready timeline
    timeline = [
        {
            "date": str(report["created_at"]),
            "severity": report["severity_level"],
            "confidence": report["confidence_score"],
            "image_url": report["image_url"]
        }
        for report in history
    ]

    return {
        "patient_id": patient_id,
        "total_reports": len(history),
        "timeline": timeline
    }