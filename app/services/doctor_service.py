from sqlalchemy import text
from app.database.connection import engine


def create_doctor(data):

    # Step 1: create user with role doctor
    user_query = text("""
        INSERT INTO users (hospital_id, role, full_name, email, phone)
        VALUES (:hospital_id, 'doctor', :full_name, :email, :phone)
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

        # Step 2: create doctor profile
        doctor_query = text("""
            INSERT INTO doctors (user_id, hospital_id, specialization, license_number)
            VALUES (:user_id, :hospital_id, :specialization, :license_number)
            RETURNING id
        """)

        doctor_result = conn.execute(doctor_query, {
            "user_id": user_id,
            "hospital_id": data.hospital_id,
            "specialization": data.specialization,
            "license_number": data.license_number
        })

        conn.commit()

        doctor_id = doctor_result.scalar()

    return {
        "doctor_id": doctor_id,
        "user_id": user_id
    }