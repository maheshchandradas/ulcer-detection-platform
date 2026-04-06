from sqlalchemy import text
from app.database.connection import engine


# CREATE ULCER REPORT
def create_ulcer_report(data):

    query = text("""
        INSERT INTO ulcer_reports
        (hospital_id, patient_id, doctor_id, image_url,
         prediction_result, confidence_score, severity_level, notes)
        VALUES
        (:hospital_id, :patient_id, :doctor_id, :image_url,
         :prediction_result, :confidence_score, :severity_level, :notes)
        RETURNING id
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {
            "hospital_id": data.hospital_id,
            "patient_id": data.patient_id,
            "doctor_id": data.doctor_id,
            "image_url": data.image_url,
            "prediction_result": data.prediction_result,
            "confidence_score": data.confidence_score,
            "severity_level": data.severity_level,
            "notes": data.notes
        })

        conn.commit()

        report_id = result.scalar()

    return report_id


# GET PATIENT HISTORY
def get_patient_history(patient_id):

    query = text("""
        SELECT
            id,
            image_url,
            prediction_result,
            confidence_score,
            severity_level,
            notes,
            created_at
        FROM ulcer_reports
        WHERE patient_id = :patient_id
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"patient_id": patient_id})
        history = result.mappings().all()

    return history