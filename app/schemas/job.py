from pydantic import BaseModel

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: str
    company_id: int