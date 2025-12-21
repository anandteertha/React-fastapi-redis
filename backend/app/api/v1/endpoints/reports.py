"""
Report endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.schemas.report import ReportResponse
from app.services.report_service import ReportService
from app.models.user import User

router = APIRouter()


@router.post("/generate", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(
    report_date: datetime = Query(default_factory=datetime.now),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate daily nutrition report"""
    return ReportService.generate_daily_report(db, current_user.id, report_date)


@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's reports"""
    return ReportService.get_user_reports(db, current_user.id, start_date, end_date)


@router.get("/today", response_model=ReportResponse)
async def get_today_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get today's report"""
    today = datetime.now().replace(hour=0, minute=0, second=0)
    report = ReportService.generate_daily_report(db, current_user.id, today)
    return report

