from sqlalchemy import Column, Integer, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Text, nullable=True)  # store vector as JSON string
    score = Column(Float, nullable=True)

    recruiter_id = Column(Integer, ForeignKey("recruiters.id"))
    recruiter = relationship("Recruiter", backref="resumes")

    job_id = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("Job", backref="resumes")

    created_at = Column(DateTime(timezone=True), server_default=func.now())