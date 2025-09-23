
import os

# Admin credentials - CHANGE THESE FOR PRODUCTION!
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

# Secret key for session management - CHANGE THIS FOR PRODUCTION!
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))

# Database configuration
DATABASE_PATH = os.environ.get('DATABASE_PATH', '/opt/render/project/src/assessments.db')

# Production settings
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
TESTING = False

# --- Email Configuration (Placeholder) ---
# For this to work, you must install Flask-Mail: pip install Flask-Mail
# You will also need to provide the credentials for your email server.
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.example.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'your-email@example.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your-email-password')
