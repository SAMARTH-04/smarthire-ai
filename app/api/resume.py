from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.utils.pdf_parser import extract_text_from_pdf
from app.services.embedding_service import generate_embedding, cosine_similarity
from app.models.resume import Resume
from app.models.job import Job
import json

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload")
async def upload_resume(
    job_id: int,
    recruiter_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Validate job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if not job.embedding:
        raise HTTPException(status_code=400, detail="Job embedding missing")

    # Extract resume text
    text = extract_text_from_pdf(file.file)

    # Generate resume embedding
    resume_embedding = generate_embedding(text)

    # Calculate similarity score
    job_embedding = json.loads(job.embedding)
    score = cosine_similarity(job_embedding, resume_embedding)

    resume = Resume(
        content=text,
        embedding=json.dumps(resume_embedding),
        recruiter_id=recruiter_id,
        job_id=job_id,
        score=score
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded and scored",
        "resume_id": resume.id,
        "similarity_score": round(score, 4)
    }