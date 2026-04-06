from sqlalchemy import text
from app.database.connection import engine


# CREATE hospital
def create_hospital(data):

    query = text("""
        INSERT INTO hospitals (name, address, contact_email, contact_phone)
        VALUES (:name, :address, :contact_email, :contact_phone)
        RETURNING id, name
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "name": data.name,
            "address": data.address,
            "contact_email": data.contact_email,
            "contact_phone": data.contact_phone
        })
        conn.commit()

        hospital = result.mappings().first()

    return hospital


# GET all hospitals
def get_hospitals():

    query = text("SELECT * FROM hospitals ORDER BY id")

    with engine.connect() as conn:
        result = conn.execute(query)
        hospitals = result.mappings().all()

    return hospitals