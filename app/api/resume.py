from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.utils.pdf_parser import extract_text_from_pdf
from app.services.embedding_service import generate_embedding
from app.models.resume import Resume
import json

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(
    job_id: int,
    recruiter_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    text = extract_text_from_pdf(file.file)
    embedding = generate_embedding(text)

    resume = Resume(
        content=text,
        embedding=json.dumps(embedding),
        recruiter_id=recruiter_id,
        job_id=job_id
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"message": "Resume uploaded and processed", "resume_id": resume.id}