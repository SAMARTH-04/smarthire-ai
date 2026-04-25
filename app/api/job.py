import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate
from app.services.embedding_service import generate_embedding

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/")
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):

    text_for_embedding = f"{job_data.title} {job_data.description} {job_data.required_skills}"
    embedding = generate_embedding(text_for_embedding)

    job = Job(
        title=job_data.title,
        description=job_data.description,
        required_skills=job_data.required_skills,
        embedding=json.dumps(embedding),
        company_id=job_data.company_id
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job