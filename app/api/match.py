from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.dependencies.database import get_db
from app.models.job import Job
from app.models.resume import Resume

router = APIRouter(prefix="/ai", tags=["AI Matching"])


@router.get("/match/{job_id}")
def get_ranked_resumes(job_id: int, db: Session = Depends(get_db)):

    # Validate Job Exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Fetch resumes for that job ordered by score
    resumes = (
        db.query(Resume)
        .filter(Resume.job_id == job_id)
        .order_by(desc(Resume.score))
        .all()
    )

    if not resumes:
        return {
            "job_id": job_id,
            "total_candidates": 0,
            "ranked_candidates": []
        }

    ranked_results = []

    for resume in resumes:
        ranked_results.append({
            "resume_id": resume.id,
            "score": round(resume.score, 4) if resume.score else 0
        })

    return {
        "job_id": job_id,
        "total_candidates": len(ranked_results),
        "ranked_candidates": ranked_results
    }