from flask import Flask
from routes import register_blueprints

def create_app():
    """Initialize Flask application."""
    app = Flask(__name__)
    register_blueprints(app)  # Register all blueprints
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
