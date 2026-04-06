from fastapi import FastAPI
from app.routes import hospital_routes, doctor_routes, patient_routes, report_routes, predict_routes
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Ulcer Detection API")

@app.get("/")
def home():
    return {"message": "Backend running"}

app.include_router(hospital_routes.router)
app.include_router(doctor_routes.router)
app.include_router(patient_routes.router)
app.include_router(report_routes.router)
app.include_router(predict_routes.router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
