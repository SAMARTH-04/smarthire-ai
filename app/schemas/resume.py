from pydantic import BaseModel

class ResumeCreate(BaseModel):
    content: str
    recruiter_id: int
    job_id: int