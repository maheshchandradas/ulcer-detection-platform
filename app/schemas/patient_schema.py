from pydantic import BaseModel
from datetime import date
from typing import Optional


class PatientCreate(BaseModel):

    hospital_id: int
    doctor_id: int
    full_name: str
    email: str
    phone: str
    date_of_birth: date
    gender: str
    medical_notes: Optional[str] = None