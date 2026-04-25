from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text, nullable=True)
    embedding = Column(Text, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", backref="jobs")

    created_at = Column(DateTime(timezone=True), server_default=func.now())