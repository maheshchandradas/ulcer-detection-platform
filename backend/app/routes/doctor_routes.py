from fastapi import APIRouter
from sqlalchemy import text
from app.database.connection import engine

from app.schemas.doctor_schema import DoctorCreate
from app.services.doctor_service import create_doctor

router = APIRouter()


@router.post("/doctors")
def add_doctor(doctor: DoctorCreate):

    result = create_doctor(doctor)

    return {
        "message": "Doctor created successfully",
        "doctor": result
    }


# API 1 — GET ALL PATIENTS OF DOCTOR
@router.get("/doctor/{doctor_id}/patients")
def get_doctor_patients(doctor_id: int):

    query = text("""
    SELECT DISTINCT 
        p.id,
        p.user_id,
        p.hospital_id,
        p.assigned_doctor_id,
        p.date_of_birth,
        p.gender,
        p.medical_notes,
        p.created_at
    FROM patients p
    JOIN ulcer_reports ur ON p.id = ur.patient_id
    WHERE ur.doctor_id = :doctor_id
""")

    with engine.connect() as conn:
        result = conn.execute(query, {"doctor_id": doctor_id})
        patients = result.mappings().all()

    return {
        "doctor_id": doctor_id,
        "total_patients": len(patients),
        "patients": patients
    }


# API 2 — GET ALL REPORTS OF DOCTOR
@router.get("/doctor/{doctor_id}/reports")
def get_doctor_reports(doctor_id: int):

    query = text("""
        SELECT
            ur.id,
            ur.patient_id,
            ur.image_url,
            ur.prediction_result,
            ur.confidence_score,
            ur.severity_level,
            ur.created_at
        FROM ulcer_reports ur
        WHERE ur.doctor_id = :doctor_id
        ORDER BY ur.created_at DESC
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"doctor_id": doctor_id})
        reports = result.mappings().all()

    return {
        "doctor_id": doctor_id,
        "total_reports": len(reports),
        "reports": reports
    }


# API 3 — DASHBOARD SUMMARY
@router.get("/doctor/{doctor_id}/dashboard")
def doctor_dashboard(doctor_id: int):

    with engine.connect() as conn:

        total_patients = conn.execute(text("""
            SELECT COUNT(DISTINCT patient_id)
            FROM ulcer_reports
            WHERE doctor_id = :doctor_id
        """), {"doctor_id": doctor_id}).scalar()

        total_reports = conn.execute(text("""
            SELECT COUNT(*)
            FROM ulcer_reports
            WHERE doctor_id = :doctor_id
        """), {"doctor_id": doctor_id}).scalar()

        severe_cases = conn.execute(text("""
            SELECT COUNT(*)
            FROM ulcer_reports
            WHERE doctor_id = :doctor_id
            AND severity_level IN ('Grade 4', 'Grade 5')
        """), {"doctor_id": doctor_id}).scalar()

    return {
        "doctor_id": doctor_id,
        "summary": {
            "total_patients": total_patients,
            "total_reports": total_reports,
            "severe_cases": severe_cases
        }
    }