"""
Daily report model - BCNF normalized
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class DailyReport(Base):
    """Daily nutrition report table - normalized to BCNF"""
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_date = Column(DateTime(timezone=True), nullable=False, index=True)
    total_calories = Column(Float, nullable=False)
    total_protein = Column(Float, nullable=False)
    total_carbs = Column(Float, nullable=False)
    total_fats = Column(Float, nullable=False)
    total_fiber = Column(Float, default=0.0)
    total_sugar = Column(Float, default=0.0)
    total_sodium = Column(Float, default=0.0)
    analysis = Column(Text)  # AI-generated analysis
    recommendations = Column(Text)  # AI-generated recommendations
    motivation_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")

