"""
CareSync Backend API - Main Application Entry Point

This module serves as the main entry point for the CareSync mental health platform backend.
It initializes the Flask application, configures database connections, sets up authentication,
and registers all API routes.

The application provides RESTful APIs for:
- User authentication and management
- Therapist profile management
- Patient registration and browsing
- Messaging system
- Appointment scheduling
- Review and rating system

Author: CareSync Development Team
Version: 1.0.0
License: MIT
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_to_db(message: str, level: str = "INFO", user_id: str = None):
    """
    Centralized logging function for database operations and application events.

    Args:
        message (str): Log message to record
        level (str): Log level (INFO, WARNING, ERROR, DEBUG)
        user_id (str, optional): ID of user associated with the log entry

    Returns:
        None
    """
    timestamp = datetime.utcnow().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "level": level,
        "message": message,
        "user_id": user_id,
        "endpoint": request.endpoint if request else None,
        "ip_address": request.remote_addr if request else None
    }

    logger.info(f"DB_LOG: {log_entry}")

    # TODO: Implement actual database logging table
    # This will be implemented when we add the logging table to our schema


# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                  'postgresql://postgres:postgres@localhost:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Redis for caching and session management
redis_client = redis.Redis.from_url(
    os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    decode_responses=True
)


# Database Models
class User(db.Model):
    """
    User model representing both therapists and patients in the system.

    This model serves as the base user table with role-based access control.
    Users can be either therapists or patients, with different permissions
    and profile information based on their role.

    Attributes:
        id (int): Primary key, unique user identifier
        email (str): User's email address (unique)
        password_hash (str): Hashed password for authentication
        role (str): User role ('therapist' or 'patient')
        is_active (bool): Whether the user account is active
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last account update timestamp
        language_preference (str): User's preferred language (he, ar, en)
        phone_number (str): User's phone number for contact
        profile_completed (bool): Whether profile setup is complete
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'therapist' or 'patient'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    language_preference = db.Column(db.String(2), default='he')  # he, ar, en
    phone_number = db.Column(db.String(20))
    profile_completed = db.Column(db.Boolean, default=False)

    # Relationships
    therapist_profile = db.relationship('TherapistProfile',
                                        backref='user',
                                        uselist=False)
    patient_profile = db.relationship('PatientProfile',
                                      backref='user',
                                      uselist=False)

    def set_password(self, password: str) -> None:
        """
        Hash and set user password.

        Args:
            password (str): Plain text password to hash

        Returns:
            None
        """
        self.password_hash = generate_password_hash(password)
        log_to_db(f"Password set for user {self.id}", "INFO", str(self.id))

    def check_password(self, password: str) -> bool:
        """
        Verify user password against stored hash.

        Args:
            password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """
        Convert user object to dictionary for API responses.

        Returns:
            dict: User data without sensitive information
        """
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'language_preference': self.language_preference,
            'phone_number': self.phone_number,
            'profile_completed': self.profile_completed
        }


class TherapistProfile(db.Model):
    """
    Therapist profile model containing professional information.

    This model stores detailed information about therapists including
    their professional credentials, specializations, availability,
    and practice details.

    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to users table
        first_name (str): Therapist's first name
        last_name (str): Therapist's last name
        license_number (str): Professional license number
        specialization (str): Primary area of specialization
        experience_years (int): Years of professional experience
        education (str): Educational background
        languages (list): Languages spoken by therapist
        availability (dict): Weekly availability schedule
        hourly_rate (float): Hourly consultation rate
        bio (str): Professional biography
        verified (bool): Whether credentials are verified
        rating (float): Average rating from patients
        total_reviews (int): Total number of reviews
    """
    __tablename__ = 'therapist_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    education = db.Column(db.Text)
    languages = db.Column(db.JSON)  # List of languages
    availability = db.Column(db.JSON)  # Weekly schedule
    hourly_rate = db.Column(db.Float)
    bio = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Convert therapist profile to dictionary for API responses.

        Returns:
            dict: Therapist profile data
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'license_number': self.license_number,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'education': self.education,
            'languages': self.languages,
            'availability': self.availability,
            'hourly_rate': self.hourly_rate,
            'bio': self.bio,
            'verified': self.verified,
            'rating': self.rating,
            'total_reviews': self.total_reviews,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class PatientProfile(db.Model):
    """
    Patient profile model containing personal information.

    This model stores information about patients including their
    personal details, preferences, and therapy history.

    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to users table
        first_name (str): Patient's first name
        last_name (str): Patient's last name
        date_of_birth (date): Patient's date of birth
        gender (str): Patient's gender
        location (str): Patient's location/city
        therapy_history (str): Previous therapy experience
        preferences (dict): Therapy preferences and requirements
        emergency_contact (str): Emergency contact information
    """
    __tablename__ = 'patient_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    location = db.Column(db.String(100))
    therapy_history = db.Column(db.Text)
    preferences = db.Column(db.JSON)  # Therapy preferences
    emergency_contact = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Convert patient profile to dictionary for API responses.

        Returns:
            dict: Patient profile data
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'location': self.location,
            'therapy_history': self.therapy_history,
            'preferences': self.preferences,
            'emergency_contact': self.emergency_contact,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# API Routes
@app.route("/api/health")
def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Application status and version information
    """
    try:
        # Test database connection
        db_status = "connected" if db.engine.pool.checkedin() > 0 else "disconnected"
    except Exception:
        db_status = "unavailable"

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": db_status
    })


@app.route("/api/auth/register", methods=['POST'])
def register():
    """
    User registration endpoint.

    Accepts POST requests with user registration data and creates
    a new user account with appropriate role and profile.

    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "secure_password",
        "role": "therapist" or "patient",
        "language_preference": "he" (optional),
        "phone_number": "+972501234567" (optional)
    }

    Returns:
        dict: Registration result with user data or error message
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required_fields = ['email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Validate role
        if data['role'] not in ['therapist', 'patient']:
            return jsonify({"error": "Invalid role. Must be 'therapist' or 'patient'"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409

        # Create new user
        user = User(
            email=data['email'],
            role=data['role'],
            language_preference=data.get('language_preference', 'he'),
            phone_number=data.get('phone_number')
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        log_to_db(f"New user registered: {user.email} with role {user.role}",
                  "INFO", str(user.id))

        return jsonify({
            "message": "User registered successfully",
            "user": user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        log_to_db(f"Registration error: {str(e)}", "ERROR")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/auth/login", methods=['POST'])
def login():
    """
    User authentication endpoint.

    Accepts POST requests with login credentials and returns
    JWT access token upon successful authentication.

    Expected JSON payload:
    {
        "email": "user@example.com",
        "password": "user_password"
    }

    Returns:
        dict: Authentication result with JWT token or error message
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required"}), 400

        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Invalid email or password"}), 401

        if not user.is_active:
            return jsonify({"error": "Account is deactivated"}), 401

        # Generate JWT token
        from flask_jwt_extended import create_access_token
        access_token = create_access_token(identity=user.id)

        log_to_db(f"User logged in: {user.email}", "INFO", str(user.id))

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        log_to_db(f"Login error: {str(e)}", "ERROR")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/therapists", methods=['GET'])
def get_therapists():
    """
    Get list of therapists with filtering and pagination.

    Query parameters:
    - page (int): Page number for pagination
    - per_page (int): Number of therapists per page
    - specialization (str): Filter by specialization
    - location (str): Filter by location
    - verified (bool): Filter by verification status
    - min_rating (float): Filter by minimum rating

    Returns:
        dict: Paginated list of therapists with metadata
    """
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        specialization = request.args.get('specialization')
        verified = request.args.get('verified', type=bool)
        min_rating = request.args.get('min_rating', type=float)

        # Build query
        query = TherapistProfile.query.join(User).filter(User.role == 'therapist')

        if specialization:
            query = query.filter(TherapistProfile.specialization.ilike(f'%{specialization}%'))

        if verified is not None:
            query = query.filter(TherapistProfile.verified == verified)

        if min_rating:
            query = query.filter(TherapistProfile.rating >= min_rating)

        # Execute query with pagination
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        therapists = [therapist.to_dict() for therapist in pagination.items]

        log_to_db(f"Therapists list requested - page {page}, filters: {request.args}", "INFO")

        return jsonify({
            "therapists": therapists,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }), 200

    except Exception as e:
        log_to_db(f"Error fetching therapists: {str(e)}", "ERROR")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/therapists/<int:therapist_id>", methods=['GET'])
def get_therapist(therapist_id):
    """
    Get detailed information about a specific therapist.

    Args:
        therapist_id (int): ID of the therapist to retrieve

    Returns:
        dict: Detailed therapist information or error message
    """
    try:
        therapist = TherapistProfile.query.get(therapist_id)

        if not therapist:
            return jsonify({"error": "Therapist not found"}), 404

        log_to_db(f"Therapist profile viewed: {therapist_id}", "INFO")

        return jsonify({
            "therapist": therapist.to_dict()
        }), 200

    except Exception as e:
        log_to_db(f"Error fetching therapist {therapist_id}: {str(e)}", "ERROR")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def index():
    """
    Root endpoint for basic application status.

    Returns:
        str: Simple status message
    """
    return jsonify({
        "message": "CareSync Backend API is running!",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/api/health",
            "auth": "/api/auth/*",
            "therapists": "/api/therapists"
        }
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    log_to_db(f"Internal server error: {str(error)}", "ERROR")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Create database tables (only if database is available)
    try:
        with app.app_context():
            db.create_all()
            log_to_db("Database tables created/verified", "INFO")
    except Exception as e:
        log_to_db(f"Database initialization failed: {str(e)}", "WARNING")
        print(f"Warning: Database initialization failed: {str(e)}")
        print("App will start without database tables. Make sure to run migrations later.")

    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
