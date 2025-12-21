"""
Script to populate database with mock data for testing
"""
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import User, Food, Meal, MealFood, UserPreference, Goal
from app.core.security import get_password_hash
from app.models.meal import MealType
from app.models.goal import GoalType

# Mock user credentials
MOCK_USERNAME = "demo_user"
MOCK_PASSWORD = "demo123"
MOCK_EMAIL = "demo@nutribite.com"

# Mock foods data
MOCK_FOODS = [
    {
        "name": "Chicken Breast",
        "description": "Lean chicken breast",
        "calories_per_100g": 165.0,
        "protein_per_100g": 31.0,
        "carbs_per_100g": 0.0,
        "fats_per_100g": 3.6,
        "fiber_per_100g": 0.0,
        "sugar_per_100g": 0.0,
        "sodium_per_100g": 74.0,
    },
    {
        "name": "Brown Rice",
        "description": "Cooked brown rice",
        "calories_per_100g": 111.0,
        "protein_per_100g": 2.6,
        "carbs_per_100g": 23.0,
        "fats_per_100g": 0.9,
        "fiber_per_100g": 1.8,
        "sugar_per_100g": 0.4,
        "sodium_per_100g": 5.0,
    },
    {
        "name": "Broccoli",
        "description": "Steamed broccoli",
        "calories_per_100g": 35.0,
        "protein_per_100g": 2.8,
        "carbs_per_100g": 7.0,
        "fats_per_100g": 0.4,
        "fiber_per_100g": 2.6,
        "sugar_per_100g": 1.5,
        "sodium_per_100g": 33.0,
    },
    {
        "name": "Salmon",
        "description": "Atlantic salmon",
        "calories_per_100g": 208.0,
        "protein_per_100g": 20.0,
        "carbs_per_100g": 0.0,
        "fats_per_100g": 12.0,
        "fiber_per_100g": 0.0,
        "sugar_per_100g": 0.0,
        "sodium_per_100g": 44.0,
    },
    {
        "name": "Sweet Potato",
        "description": "Baked sweet potato",
        "calories_per_100g": 90.0,
        "protein_per_100g": 2.0,
        "carbs_per_100g": 21.0,
        "fats_per_100g": 0.2,
        "fiber_per_100g": 3.3,
        "sugar_per_100g": 4.2,
        "sodium_per_100g": 54.0,
    },
    {
        "name": "Greek Yogurt",
        "description": "Plain Greek yogurt",
        "calories_per_100g": 59.0,
        "protein_per_100g": 10.0,
        "carbs_per_100g": 3.6,
        "fats_per_100g": 0.4,
        "fiber_per_100g": 0.0,
        "sugar_per_100g": 3.6,
        "sodium_per_100g": 36.0,
    },
    {
        "name": "Oatmeal",
        "description": "Cooked oatmeal",
        "calories_per_100g": 68.0,
        "protein_per_100g": 2.4,
        "carbs_per_100g": 12.0,
        "fats_per_100g": 1.4,
        "fiber_per_100g": 1.7,
        "sugar_per_100g": 0.5,
        "sodium_per_100g": 5.0,
    },
    {
        "name": "Eggs",
        "description": "Large whole eggs",
        "calories_per_100g": 155.0,
        "protein_per_100g": 13.0,
        "carbs_per_100g": 1.1,
        "fats_per_100g": 11.0,
        "fiber_per_100g": 0.0,
        "sugar_per_100g": 1.1,
        "sodium_per_100g": 124.0,
    },
    {
        "name": "Banana",
        "description": "Medium banana",
        "calories_per_100g": 89.0,
        "protein_per_100g": 1.1,
        "carbs_per_100g": 23.0,
        "fats_per_100g": 0.3,
        "fiber_per_100g": 2.6,
        "sugar_per_100g": 12.2,
        "sodium_per_100g": 1.0,
    },
    {
        "name": "Almonds",
        "description": "Raw almonds",
        "calories_per_100g": 579.0,
        "protein_per_100g": 21.0,
        "carbs_per_100g": 22.0,
        "fats_per_100g": 50.0,
        "fiber_per_100g": 12.0,
        "sugar_per_100g": 4.4,
        "sodium_per_100g": 1.0,
    },
]


def get_or_create_food(db: Session, food_data: dict) -> Food:
    """Get existing food or create new one"""
    food = db.query(Food).filter(Food.name == food_data["name"]).first()
    if not food:
        food = Food(**food_data)
        db.add(food)
        db.commit()
        db.refresh(food)
    return food


def create_mock_user(db: Session) -> User:
    """Create or get mock user"""
    user = db.query(User).filter(User.username == MOCK_USERNAME).first()
    if user:
        print(f"User '{MOCK_USERNAME}' already exists. Using existing user.")
        return user
    
    hashed_password = get_password_hash(MOCK_PASSWORD)
    user = User(
        email=MOCK_EMAIL,
        username=MOCK_USERNAME,
        hashed_password=hashed_password,
        full_name="Demo User",
        age=30,
        gender="male",
        height_cm=175,
        weight_kg=75,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {MOCK_USERNAME}")
    return user


def create_mock_meals(db: Session, user: User, foods: dict):
    """Create mock meals for the past 7 days"""
    meal_types = [MealType.BREAKFAST, MealType.LUNCH, MealType.DINNER, MealType.SNACK]
    meal_combinations = [
        # Breakfast combinations
        [
            {"food": "Oatmeal", "quantity": 150},
            {"food": "Banana", "quantity": 120},
            {"food": "Greek Yogurt", "quantity": 200},
        ],
        [
            {"food": "Eggs", "quantity": 200},
            {"food": "Sweet Potato", "quantity": 150},
        ],
        # Lunch combinations
        [
            {"food": "Chicken Breast", "quantity": 200},
            {"food": "Brown Rice", "quantity": 150},
            {"food": "Broccoli", "quantity": 200},
        ],
        [
            {"food": "Salmon", "quantity": 200},
            {"food": "Sweet Potato", "quantity": 200},
            {"food": "Broccoli", "quantity": 150},
        ],
        # Dinner combinations
        [
            {"food": "Chicken Breast", "quantity": 250},
            {"food": "Brown Rice", "quantity": 200},
            {"food": "Broccoli", "quantity": 200},
        ],
        [
            {"food": "Salmon", "quantity": 250},
            {"food": "Sweet Potato", "quantity": 200},
        ],
        # Snack combinations
        [
            {"food": "Almonds", "quantity": 30},
        ],
        [
            {"food": "Greek Yogurt", "quantity": 150},
            {"food": "Banana", "quantity": 100},
        ],
    ]
    
    created_meals = 0
    for day_offset in range(7):
        date = datetime.now() - timedelta(days=day_offset)
        
        # Create 2-3 meals per day
        meals_today = meal_combinations[:3] if day_offset < 3 else meal_combinations[3:6]
        
        for meal_idx, meal_combo in enumerate(meals_today):
            meal_type = meal_types[meal_idx % len(meal_types)]
            meal_time = date.replace(
                hour=7 + meal_idx * 5,  # 7am, 12pm, 5pm, 10pm
                minute=0,
                second=0,
                microsecond=0
            )
            
            meal = Meal(
                user_id=user.id,
                meal_type=meal_type,
                meal_date=meal_time,
                notes=f"Mock meal for {meal_time.strftime('%Y-%m-%d')}"
            )
            db.add(meal)
            db.flush()  # Get meal.id
            
            # Add foods to meal
            for food_item in meal_combo:
                food = foods[food_item["food"]]
                meal_food = MealFood(
                    meal_id=meal.id,
                    food_id=food.id,
                    quantity_g=food_item["quantity"]
                )
                db.add(meal_food)
            
            created_meals += 1
    
    db.commit()
    print(f"Created {created_meals} meals for the past 7 days")


def create_mock_preferences(db: Session, user: User):
    """Create mock user preferences"""
    preference = db.query(UserPreference).filter(UserPreference.user_id == user.id).first()
    if preference:
        print("User preferences already exist. Skipping.")
        return
    
    preference = UserPreference(
        user_id=user.id,
        target_calories=2200.0,
        target_protein=150.0,
        target_carbs=250.0,
        target_fats=70.0,
        preferred_meal_times="Breakfast: 8am, Lunch: 1pm, Dinner: 7pm"
    )
    db.add(preference)
    db.commit()
    print("Created user preferences")


def create_mock_goals(db: Session, user: User):
    """Create mock user goals"""
    goal = db.query(Goal).filter(Goal.user_id == user.id, Goal.is_active == True).first()
    if goal:
        print("Active goal already exists. Skipping.")
        return
    
    goal = Goal(
        user_id=user.id,
        goal_type=GoalType.WEIGHT_LOSS,
        target_weight_kg=70.0,
        current_weight_kg=75.0,
        target_date=datetime.now() + timedelta(days=90),
        is_active=True
    )
    db.add(goal)
    db.commit()
    print("Created user goal")


def main():
    """Main function to populate mock data"""
    print("=" * 50)
    print("Populating database with mock data...")
    print("=" * 50)
    
    db: Session = SessionLocal()
    
    try:
        # Create or get user
        user = create_mock_user(db)
        
        # Create or get foods
        print("\nCreating foods...")
        foods = {}
        for food_data in MOCK_FOODS:
            food = get_or_create_food(db, food_data)
            foods[food.name] = food
            print(f"  + {food.name}")
        
        # Create meals
        print("\nCreating meals...")
        create_mock_meals(db, user, foods)
        
        # Create preferences
        print("\nCreating preferences...")
        create_mock_preferences(db, user)
        
        # Create goals
        print("\nCreating goals...")
        create_mock_goals(db, user)
        
        print("\n" + "=" * 50)
        print("SUCCESS: Mock data population completed!")
        print("=" * 50)
        print(f"\nLogin Credentials:")
        print(f"   Username: {MOCK_USERNAME}")
        print(f"   Password: {MOCK_PASSWORD}")
        print(f"   Email: {MOCK_EMAIL}")
        print("=" * 50)
        
    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()

