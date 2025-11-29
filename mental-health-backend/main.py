from fastapi import FastAPI
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    user_routes,
    assessment_routes,
    doctor_routes,
    consultation_routes,
    prescription_routes,
    pharmacy_routes,
    emergency_routes,
    login_routes,
    mood_routes,
    admin_routes
)

# FastAPI app instance
app = FastAPI(
    title="Mental Health Support API",
    description="Backend for the Mental Health Assessment and Consultation System",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)
origins = [
    "https://opulent-goggles-g4q7r9vvg4qw2r77-3000.app.github.dev",  # Frontend
    "https://opulent-goggles-g4q7r9vvg4qw2r77-3001.app.github.dev",  # If frontend re-runs on 3001
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(user_routes.router)
app.include_router(assessment_routes.router)
app.include_router(doctor_routes.router)
app.include_router(consultation_routes.router)
app.include_router(prescription_routes.router)
app.include_router(pharmacy_routes.router)
app.include_router(emergency_routes.router)
app.include_router(login_routes.router)
app.include_router(mood_routes.router)
app.include_router(admin_routes.router)
@app.get("/")
def root():
    return {"message": "Mental Health Support API is running successfully!"}
