from flask import Flask
from .products import products_bp

def register_blueprints(app: Flask):
    """
    Register all blueprints to the Flask application.
    Args:
        app (Flask): The Flask app instance.
    """
    app.register_blueprint(products_bp, url_prefix="/products")
