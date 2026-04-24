from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.recruiter import Recruiter
from app.models.company import Company
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(email: str, password: str, company_name: str, db: Session = Depends(get_db)):
    
    existing = db.query(Recruiter).filter(Recruiter.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    company = Company(name=company_name)
    db.add(company)
    db.commit()
    db.refresh(company)

    recruiter = Recruiter(
        email=email,
        hashed_password=hash_password(password),
        company_id=company.id,
        is_admin=True
    )

    db.add(recruiter)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    
    recruiter = db.query(Recruiter).filter(Recruiter.email == email).first()
    
    if not recruiter or not verify_password(password, recruiter.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": recruiter.email})
    
    return {"access_token": token}