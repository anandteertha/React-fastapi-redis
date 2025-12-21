# Backend Environment Setup Guide

This guide will help you set up the `.env` file for the NutriBite backend application.

## Quick Start

1. Copy the `.env` file template (if you don't have one, create it in the `backend` directory)
2. Update the required variables with your actual values
3. Generate a secure secret key
4. Start the application

## Environment Variables

### Required Variables

These variables **must** be set for the application to work:

#### `DATABASE_URL`
MySQL database connection string.

**Format:** `mysql+pymysql://username:password@host:port/database_name`

**Example:**
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/nutribite
```

**Setup Steps:**
1. Make sure MySQL is installed and running
2. Create the database: `CREATE DATABASE nutribite;`
3. Run the schema: `mysql -u root -p nutribite < database/schema.sql`
4. Update the connection string with your MySQL credentials

#### `SECRET_KEY`
Secret key used for JWT token encryption. **Never share this key or commit it to version control.**

**Generate a secure key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Example:**
```env
SECRET_KEY=your-generated-secret-key-here
```

### Optional Variables

These have default values but can be customized:

#### `REDIS_URL`
Redis connection URL for caching (default: `redis://localhost:6379/0`)

```env
REDIS_URL=redis://localhost:6379/0
```

#### `OPENAI_API_KEY`
API key for OpenAI (required only if using AI recommendation features)

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

#### `ALGORITHM`
JWT algorithm (default: `HS256`)

```env
ALGORITHM=HS256
```

#### `ACCESS_TOKEN_EXPIRE_MINUTES`
JWT token expiration time in minutes (default: `30`)

```env
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### `ENVIRONMENT`
Application environment: `development` or `production` (default: `development`)

```env
ENVIRONMENT=development
```

#### `DEBUG`
Enable debug mode (default: `True`)

```env
DEBUG=True
```

#### `CORS_ORIGINS`
Comma-separated list of allowed frontend origins

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Complete .env File Template

```env
# NutriBite Backend Environment Variables

# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/nutribite

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration (optional, for AI recommendations)
OPENAI_API_KEY=

# Application Configuration
ENVIRONMENT=development
DEBUG=True

# CORS Origins (comma-separated list)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Setup Checklist

- [ ] MySQL is installed and running
- [ ] Database `nutribite` is created
- [ ] Database schema is applied (`database/schema.sql`)
- [ ] `.env` file is created in the `backend` directory
- [ ] `DATABASE_URL` is configured with correct credentials
- [ ] `SECRET_KEY` is generated and set
- [ ] Redis is installed and running (if using caching)
- [ ] `OPENAI_API_KEY` is set (if using AI features)
- [ ] All environment variables are configured

## Verification

After setting up your `.env` file, verify the configuration:

1. Start the application:
   ```bash
   cd backend
   python run.py
   ```

2. Check the health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

3. View API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Security Notes

⚠️ **Important Security Reminders:**

- Never commit the `.env` file to version control
- Use strong, randomly generated `SECRET_KEY` values
- In production, set `DEBUG=False` and `ENVIRONMENT=production`
- Keep your database credentials secure
- Rotate your `SECRET_KEY` periodically in production

## Troubleshooting

### Database Connection Errors
- Verify MySQL is running: `mysql -u root -p`
- Check database exists: `SHOW DATABASES;`
- Verify credentials in `DATABASE_URL`

### Redis Connection Errors
- Verify Redis is running: `redis-cli ping`
- Check `REDIS_URL` format is correct

### JWT Token Errors
- Ensure `SECRET_KEY` is set and not empty
- Verify `ALGORITHM` matches your security requirements

## Need Help?

If you encounter issues:
1. Check the application logs for error messages
2. Verify all required environment variables are set
3. Ensure all services (MySQL, Redis) are running
4. Review the API documentation at `/docs` endpoint

