from fastapi import APIRouter
from app.schemas.hospital_schema import HospitalCreate
from app.services.hospital_service import create_hospital, get_hospitals

router = APIRouter()


# POST hospital
@router.post("/hospitals")
def add_hospital(hospital: HospitalCreate):

    new_hospital = create_hospital(hospital)

    return {
        "message": "Hospital created successfully",
        "hospital": new_hospital
    }


# GET hospitals
@router.get("/hospitals")
def list_hospitals():

    hospitals = get_hospitals()

    return {
        "total": len(hospitals),
        "data": hospitals
    }