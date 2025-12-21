"""
Daily report model - BCNF normalized
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class DailyReport(Base):
    """Daily nutrition report table - normalized to BCNF"""
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_date = Column(DateTime(timezone=True), nullable=False, index=True)
    total_calories = Column(Numeric(10, 2), nullable=False)
    total_protein = Column(Numeric(10, 2), nullable=False)
    total_carbs = Column(Numeric(10, 2), nullable=False)
    total_fats = Column(Numeric(10, 2), nullable=False)
    total_fiber = Column(Numeric(10, 2), default=0.0)
    total_sugar = Column(Numeric(10, 2), default=0.0)
    total_sodium = Column(Numeric(10, 2), default=0.0)
    analysis = Column(Text)  # AI-generated analysis
    recommendations = Column(Text)  # AI-generated recommendations
    motivation_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reports")

