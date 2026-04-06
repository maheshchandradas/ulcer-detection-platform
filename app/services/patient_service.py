from sqlalchemy import text
from app.database.connection import engine


# CREATE PATIENT
def create_patient(data):

    user_query = text("""
        INSERT INTO users (hospital_id, role, full_name, email, phone)
        VALUES (:hospital_id, 'patient', :full_name, :email, :phone)
        RETURNING id
    """)

    with engine.connect() as conn:

        user_result = conn.execute(user_query, {
            "hospital_id": data.hospital_id,
            "full_name": data.full_name,
            "email": data.email,
            "phone": data.phone
        })

        user_id = user_result.scalar()

        patient_query = text("""
            INSERT INTO patients
            (user_id, hospital_id, assigned_doctor_id, date_of_birth, gender, medical_notes)
            VALUES
            (:user_id, :hospital_id, :doctor_id, :date_of_birth, :gender, :medical_notes)
            RETURNING id
        """)

        patient_result = conn.execute(patient_query, {
            "user_id": user_id,
            "hospital_id": data.hospital_id,
            "doctor_id": data.doctor_id,
            "date_of_birth": data.date_of_birth,
            "gender": data.gender,
            "medical_notes": data.medical_notes
        })

        conn.commit()

        patient_id = patient_result.scalar()

    return {
        "patient_id": patient_id,
        "user_id": user_id
    }


# GET PATIENT BY ID
def get_patient_by_id(patient_id):

    query = text("""
        SELECT 
            p.id AS patient_id,
            u.full_name,
            u.email,
            u.phone,
            p.date_of_birth,
            p.gender,
            p.medical_notes,
            d.id AS doctor_id,
            du.full_name AS doctor_name,
            h.id AS hospital_id,
            h.name AS hospital_name
        FROM patients p
        JOIN users u ON p.user_id = u.id
        JOIN doctors d ON p.assigned_doctor_id = d.id
        JOIN users du ON d.user_id = du.id
        JOIN hospitals h ON p.hospital_id = h.id
        WHERE p.id = :patient_id
    """)

    with engine.connect() as conn:

        result = conn.execute(query, {"patient_id": patient_id})
        patient = result.mappings().first()

    return patient