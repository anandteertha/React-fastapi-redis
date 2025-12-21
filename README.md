# NutriBite

<div align="center">

[![CI/CD](https://img.shields.io/github/actions/workflow/status/yourusername/NutriBite/ci.yml?branch=main&label=CI%2FCD&logo=github)](https://github.com/yourusername/NutriBite/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Redis](https://img.shields.io/badge/Redis-7+-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A comprehensive nutrition tracking and recommendation application**

*Built with FastAPI, React, MySQL, and Redis*

[Features](#features) • [Setup](#setup) • [API Docs](#api-documentation) • [Tests](#running-tests)

</div>

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

2. Create and activate virtual environment:
```bash
python -m venv nutribite
# On Windows:
.\nutribite\Scripts\Activate.ps1
# On Linux/Mac:
source nutribite/bin/activate
```

3. Install dependencies:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration (DATABASE_URL, REDIS_URL, SECRET_KEY, etc.)
```

5. Set up database:
```bash
mysql -u root -p < database/schema.sql
```

6. Run the server:
```bash
python run.py
# Or: uvicorn app.main:app --reload
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

## Development

### Running in Development Mode

**Backend:**
```bash
cd backend
.\nutribite\Scripts\Activate.ps1  # Windows
python run.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Follow SOLID principles
2. Write tests for new features
3. Update documentation
4. Ensure all tests pass
5. Follow the existing code style

## Project Status

✅ Backend API complete  
✅ Frontend UI complete  
✅ Database schema implemented  
✅ RAG recommender integrated  
✅ Test suite configured  
✅ CI/CD pipeline set up  

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note:** Update the GitHub username in the badges above (`yourusername`) to match your repository.
