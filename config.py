import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration loaded from environment variables."""
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fixmycar-dev-fallback-key-for-local-development-only')

    # Normalize Render's legacy postgres:// URLs to postgresql://
    raw_db_url = os.environ.get('DATABASE_URL')
    if raw_db_url:
        if raw_db_url.startswith('postgres://'):
            raw_db_url = raw_db_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        # SQLite fallback for local development if PostgreSQL is not set
        SQLALCHEMY_DATABASE_URI = 'sqlite:///fixmycar.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security settings
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # When deployed on Render or behind HTTPS in production, enforce Secure cookies
    SESSION_COOKIE_SECURE = (
        os.environ.get('FLASK_ENV') == 'production' 
        or os.environ.get('RENDER') is not None
        or os.environ.get('SESSION_COOKIE_SECURE', '').lower() in ('true', '1')
    )

    # Debug mode is explicitly controlled by FLASK_DEBUG env var, defaulting to False in production
    DEBUG = os.environ.get('FLASK_DEBUG', '0') in ('true', '1', 'True')
