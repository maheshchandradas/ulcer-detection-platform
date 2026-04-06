from pydantic import BaseModel

class DoctorCreate(BaseModel):
    hospital_id: int
    full_name: str
    email: str
    phone: str
    specialization: str
    license_number: str