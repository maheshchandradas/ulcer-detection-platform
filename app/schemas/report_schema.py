from pydantic import BaseModel
from typing import Optional


class UlcerReportCreate(BaseModel):

    hospital_id: int
    patient_id: int
    doctor_id: int
    image_url: str
    prediction_result: str
    confidence_score: float
    severity_level: str
    notes: Optional[str] = None