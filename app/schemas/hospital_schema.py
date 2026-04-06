from pydantic import BaseModel
from typing import Optional

class HospitalCreate(BaseModel):
    name: str
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
