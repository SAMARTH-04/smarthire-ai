from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.api.auth import router as auth_router

app = FastAPI(title="SmartHire AI")
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "SmartHire AI running"}

@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"message": "Database connected successfully"}