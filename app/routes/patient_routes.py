from fastapi import APIRouter
from app.schemas.patient_schema import PatientCreate
from app.services.patient_service import create_patient, get_patient_by_id
router = APIRouter()


# CREATE PATIENT
@router.post("/patients")
def add_patient(patient: PatientCreate):

    result = create_patient(patient)

    return {
        "message": "Patient created successfully",
        "patient": result
    }

# GET PATIENT BY ID
@router.get("/patients/{patient_id}")
def get_patient(patient_id: int):

    patient = get_patient_by_id(patient_id)

    return {
        "patient": patient
    }