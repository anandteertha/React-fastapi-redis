"""
Report service - follows SOLID principles
Single Responsibility: Handles daily report generation
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from app.models.report import DailyReport
from app.models.meal import Meal
from app.services.meal_service import MealService


class ReportService:
    """Service for report operations"""
    
    @staticmethod
    def generate_daily_report(
        db: Session,
        user_id: int,
        report_date: datetime
    ) -> DailyReport:
        """Generate daily nutrition report"""
        # Get all meals for the day
        start_date = report_date.replace(hour=0, minute=0, second=0)
        end_date = report_date.replace(hour=23, minute=59, second=59)
        
        meals = MealService.get_user_meals(db, user_id, start_date, end_date)
        
        # Calculate totals
        total_calories = 0.0
        total_protein = 0.0
        total_carbs = 0.0
        total_fats = 0.0
        total_fiber = 0.0
        total_sugar = 0.0
        total_sodium = 0.0
        
        for meal in meals:
            nutrition = MealService.calculate_meal_nutrition(meal)
            total_calories += nutrition["total_calories"]
            total_protein += nutrition["total_protein"]
            total_carbs += nutrition["total_carbs"]
            total_fats += nutrition["total_fats"]
        
        # Get user preferences for comparison
        from app.services.preference_service import PreferenceService
        preferences = PreferenceService.get_user_preferences(db, user_id)
        
        # Generate analysis and recommendations
        analysis = ReportService._generate_analysis(
            total_calories,
            total_protein,
            preferences
        )
        
        recommendations = ReportService._generate_recommendations(
            total_calories,
            total_protein,
            preferences
        )
        
        motivation = ReportService._generate_motivation_message(
            total_calories,
            total_protein,
            preferences
        )
        
        # Create or update report
        existing_report = db.query(DailyReport).filter(
            DailyReport.user_id == user_id,
            DailyReport.report_date >= start_date,
            DailyReport.report_date <= end_date
        ).first()
        
        if existing_report:
            existing_report.total_calories = total_calories
            existing_report.total_protein = total_protein
            existing_report.total_carbs = total_carbs
            existing_report.total_fats = total_fats
            existing_report.analysis = analysis
            existing_report.recommendations = recommendations
            existing_report.motivation_message = motivation
            db.commit()
            db.refresh(existing_report)
            return existing_report
        else:
            new_report = DailyReport(
                user_id=user_id,
                report_date=report_date,
                total_calories=total_calories,
                total_protein=total_protein,
                total_carbs=total_carbs,
                total_fats=total_fats,
                total_fiber=total_fiber,
                total_sugar=total_sugar,
                total_sodium=total_sodium,
                analysis=analysis,
                recommendations=recommendations,
                motivation_message=motivation
            )
            db.add(new_report)
            db.commit()
            db.refresh(new_report)
            return new_report
    
    @staticmethod
    def _generate_analysis(
        total_calories: float,
        total_protein: float,
        preferences: Optional
    ) -> str:
        """Generate analysis text"""
        if not preferences:
            return f"Today you consumed {total_calories:.0f} calories and {total_protein:.0f}g of protein."
        
        calorie_diff = total_calories - (preferences.target_calories or 0)
        protein_diff = total_protein - (preferences.target_protein or 0)
        
        analysis = f"Today you consumed {total_calories:.0f} calories"
        if preferences.target_calories:
            if calorie_diff > 0:
                analysis += f" ({calorie_diff:.0f} over your target)"
            elif calorie_diff < 0:
                analysis += f" ({abs(calorie_diff):.0f} under your target)"
            else:
                analysis += " (right on target!)"
        
        analysis += f" and {total_protein:.0f}g of protein"
        if preferences.target_protein:
            if protein_diff > 0:
                analysis += f" ({protein_diff:.0f}g over target)"
            elif protein_diff < 0:
                analysis += f" ({abs(protein_diff):.0f}g under target)"
            else:
                analysis += " (target met!)"
        
        return analysis
    
    @staticmethod
    def _generate_recommendations(
        total_calories: float,
        total_protein: float,
        preferences: Optional
    ) -> str:
        """Generate recommendations"""
        recommendations = []
        
        if preferences:
            if total_calories < (preferences.target_calories or 0) * 0.8:
                recommendations.append("Consider adding a healthy snack to meet your calorie goals")
            elif total_calories > (preferences.target_calories or 0) * 1.2:
                recommendations.append("Try to reduce portion sizes or choose lower-calorie options")
            
            if total_protein < (preferences.target_protein or 0) * 0.8:
                recommendations.append("Add more protein-rich foods like chicken, fish, or legumes")
        
        if not recommendations:
            recommendations.append("Keep up the great work! Your nutrition is on track.")
        
        return " ".join(recommendations)
    
    @staticmethod
    def _generate_motivation_message(
        total_calories: float,
        total_protein: float,
        preferences: Optional
    ) -> str:
        """Generate motivation message"""
        messages = [
            "Every meal is a step toward your goals!",
            "You're making great progress!",
            "Consistency is key - keep it up!",
            "Your dedication is paying off!",
            "Small steps lead to big changes!"
        ]
        
        if preferences and preferences.target_calories:
            if abs(total_calories - preferences.target_calories) < preferences.target_calories * 0.1:
                return "Perfect! You hit your calorie target today. Excellent work! 🎉"
        
        import random
        return random.choice(messages)
    
    @staticmethod
    def get_user_reports(
        db: Session,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[DailyReport]:
        """Get user's reports within date range"""
        query = db.query(DailyReport).filter(DailyReport.user_id == user_id)
        
        if start_date:
            query = query.filter(DailyReport.report_date >= start_date)
        if end_date:
            query = query.filter(DailyReport.report_date <= end_date)
        
        return query.order_by(DailyReport.report_date.desc()).all()

