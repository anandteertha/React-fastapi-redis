# NutriBite

A comprehensive nutrition tracking and recommendation application built with FastAPI, React, MySQL, and Redis.

## Features

- **FastAPI Backend**: RESTful API with MySQL database and Redis caching
- **BCNF-Normalized Database**: Efficient, normalized MySQL schema
- **React Frontend**: Modern, responsive UI with reusable components
- **RAG-Based Recommender**: AI-powered food recommendations using Retrieval-Augmented Generation
- **User Preferences**: Customizable food preferences and dietary restrictions
- **Daily Reports**: Automated nutrition analysis and recommendations
- **SOLID Principles**: Clean, maintainable code following SOLID principles
- **Comprehensive Testing**: Pytest for backend, Cypress for frontend
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy (ORM)
- MySQL
- Redis (caching/sessions)
- Pydantic (validation)
- LangChain (RAG)
- OpenAI API
- Pytest

### Frontend
- React 18
- React Router
- TanStack Query (React Query)
- Axios
- Vite
- Cypress

## Project Structure

```
NutriBite/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── database/
│   │   └── schema.sql    # Database schema
│   ├── tests/            # Pytest tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── contexts/     # React contexts
│   │   ├── pages/        # Page components
│   │   └── services/     # API services
│   ├── cypress/          # Cypress tests
│   └── package.json
└── .github/
    └── workflows/        # CI/CD pipelines
```

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- Redis 7+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up database:
```bash
mysql -u root -p < database/schema.sql
```

6. Run the server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run test        # Headless mode
npm run test:open   # Interactive mode
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

The database follows BCNF (Boyce-Codd Normal Form) normalization:
- **Users**: User accounts and profiles
- **Foods**: Food catalog with nutrition information
- **Meals**: Meal instances
- **MealFoods**: Junction table for meals and foods
- **UserPreferences**: User nutrition targets and preferences
- **DietaryRestrictions**: User dietary restrictions
- **Goals**: User fitness goals
- **DailyReports**: Daily nutrition summaries

## Key Features

### Reusable Components
- **FoodSelector**: Search and select foods with quantity
- **PreferenceForm**: Manage user preferences and dietary restrictions

### RAG Recommender
The recommender uses Retrieval-Augmented Generation to provide personalized food recommendations based on:
- User preferences
- Dietary restrictions
- Target calories
- Historical meal data

### Caching Strategy
- User data cached in Redis
- Food search results cached
- Meal data cached for performance

## CI/CD

The project includes GitHub Actions workflows for:
- Automated backend testing
- Frontend build and Cypress tests
- Code linting
- Coverage reporting

## Contributing

1. Follow SOLID principles
2. Write tests for new features
3. Update documentation
4. Ensure all tests pass

## License

MIT License
