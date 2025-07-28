# INNERA Backend API Documentation

## Overview

The INNERA Backend API provides RESTful endpoints for the mental health platform, enabling user authentication, therapist management, patient registration, and core platform functionality.

**Base URL**: `http://localhost:5000/api`

**Authentication**: JWT Bearer tokens for protected endpoints

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Creates a new user account with specified role (therapist or patient).

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "role": "therapist",
  "language_preference": "he",
  "phone_number": "+972501234567"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "therapist",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "language_preference": "he",
    "phone_number": "+972501234567",
    "profile_completed": false
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields or invalid data
- `409 Conflict`: User with email already exists

### Login User
**POST** `/auth/login`

Authenticates user credentials and returns JWT access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "therapist",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "language_preference": "he",
    "phone_number": "+972501234567",
    "profile_completed": false
  }
}
```

**Error Responses:**
- `400 Bad Request`: Missing email or password
- `401 Unauthorized`: Invalid credentials or deactivated account

## Therapist Endpoints

### Get Therapists List
**GET** `/therapists`

Retrieves paginated list of therapists with optional filtering.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 10, max: 50)
- `specialization` (str): Filter by specialization
- `location` (str): Filter by location
- `verified` (bool): Filter by verification status
- `min_rating` (float): Filter by minimum rating

**Example Request:**
```
GET /api/therapists?page=1&per_page=10&specialization=anxiety&verified=true
```

**Response (200 OK):**
```json
{
  "therapists": [
    {
      "id": 1,
      "user_id": 1,
      "first_name": "דוד",
      "last_name": "כהן",
      "license_number": "12345",
      "specialization": "anxiety disorders",
      "experience_years": 8,
      "education": "PhD in Clinical Psychology",
      "languages": ["he", "en"],
      "availability": {
        "monday": ["09:00-12:00", "14:00-17:00"],
        "tuesday": ["09:00-12:00"],
        "wednesday": ["14:00-17:00"]
      },
      "hourly_rate": 250.0,
      "bio": "Experienced therapist specializing in anxiety disorders...",
      "verified": true,
      "rating": 4.8,
      "total_reviews": 45,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### Get Therapist Details
**GET** `/therapists/{therapist_id}`

Retrieves detailed information about a specific therapist.

**Response (200 OK):**
```json
{
  "therapist": {
    "id": 1,
    "user_id": 1,
    "first_name": "דוד",
    "last_name": "כהן",
    "license_number": "12345",
    "specialization": "anxiety disorders",
    "experience_years": 8,
    "education": "PhD in Clinical Psychology",
    "languages": ["he", "en"],
    "availability": {
      "monday": ["09:00-12:00", "14:00-17:00"],
      "tuesday": ["09:00-12:00"],
      "wednesday": ["14:00-17:00"]
    },
    "hourly_rate": 250.0,
    "bio": "Experienced therapist specializing in anxiety disorders...",
    "verified": true,
    "rating": 4.8,
    "total_reviews": 45,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Error Responses:**
- `404 Not Found`: Therapist not found

## System Endpoints

### Health Check
**GET** `/health`

Returns application health status and version information.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

## Error Handling

All endpoints return consistent error responses:

**Error Response Format:**
```json
{
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate email)
- `500 Internal Server Error`: Server error

## Authentication

Protected endpoints require JWT Bearer token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

**Token Expiration**: 1 hour (3600 seconds)

## Rate Limiting

API endpoints are rate-limited to prevent abuse:
- 200 requests per day
- 50 requests per hour
- 10 requests per minute

## Data Models

### User Model
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "therapist|patient",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "language_preference": "he|ar|en",
  "phone_number": "+972501234567",
  "profile_completed": false
}
```

### Therapist Profile Model
```json
{
  "id": 1,
  "user_id": 1,
  "first_name": "דוד",
  "last_name": "כהן",
  "license_number": "12345",
  "specialization": "anxiety disorders",
  "experience_years": 8,
  "education": "PhD in Clinical Psychology",
  "languages": ["he", "en"],
  "availability": {
    "monday": ["09:00-12:00", "14:00-17:00"]
  },
  "hourly_rate": 250.0,
  "bio": "Professional biography...",
  "verified": true,
  "rating": 4.8,
  "total_reviews": 45
}
```

### Patient Profile Model
```json
{
  "id": 1,
  "user_id": 2,
  "first_name": "שרה",
  "last_name": "לוי",
  "date_of_birth": "1990-05-15",
  "gender": "female",
  "location": "תל אביב",
  "therapy_history": "Previous therapy experience...",
  "preferences": {
    "specialization": ["anxiety", "depression"],
    "language": "he",
    "location": "תל אביב"
  },
  "emergency_contact": "+972501234567"
}
```

## Development Notes

### Environment Setup
1. Copy `env.example` to `.env`
2. Update database and Redis URLs
3. Generate secure secret keys
4. Install dependencies: `pip install -r requirements.txt`

### Database Setup
```bash
# Create database tables
flask db init
flask db migrate
flask db upgrade
```

### Running the Application
```bash
# Development mode
python main.py

# Production mode
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.
```

## Security Considerations

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **JWT Tokens**: Secure token-based authentication
3. **CORS**: Configured for cross-origin requests
4. **Input Validation**: All inputs are validated
5. **Rate Limiting**: Prevents API abuse
6. **Logging**: Comprehensive logging for security monitoring

## Future Endpoints

The following endpoints will be implemented in future versions:
- `/api/profiles/therapist` - Therapist profile management
- `/api/profiles/patient` - Patient profile management
- `/api/messages` - Messaging system
- `/api/appointments` - Appointment scheduling
- `/api/reviews` - Review and rating system
- `/api/notifications` - Notification system 