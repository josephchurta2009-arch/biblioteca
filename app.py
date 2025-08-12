import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    # Create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Configure the database with SQLite fallback
    database_url = os.environ.get("DATABASE_URL")
    
    # Force SQLite if PostgreSQL endpoint is disabled
    if not database_url or "ep-withered-cake-a5nldhc4" in database_url:
        database_url = "sqlite:///library.db"
        logging.info("Using SQLite database for reliable operation")
    else:
        logging.info(f"Using database: {database_url[:50]}...")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the app with the extension
    db.init_app(app)

    return app

# Create app instance
app = create_app()

# Import models and routes after app creation to avoid circular imports
with app.app_context():
    try:
        # Import models first
        import models  # noqa: F401
        
        # Test database connection and create tables
        db.create_all()
        logging.info("Database tables created successfully")
        
        # Import routes after successful database setup
        import routes  # noqa: F401
        
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        logging.info("Continuing with limited functionality - some features may not work")
        
        # Still import routes for basic functionality
        try:
            import routes  # noqa: F401
        except Exception as route_error:
            logging.error(f"Failed to import routes: {route_error}")
            pass
