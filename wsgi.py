#!/usr/bin/env python3
"""
WSGI configuration for the Assessment Application
This file is used by web servers to serve the Flask application in production.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Initialize database tables within app context
with app.app_context():
    from app import create_tables
    create_tables()

# WSGI application - this is what gunicorn will look for
application = app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)