from flask import Flask
from routes import products_bp


def register_blueprints(app: Flask):
    """
    Register all blueprints to Flask
    """
    app.register_blueprint(products_bp, url_prefix="/products")


def create_app():
    """
    Initialize Flask application
    """
    app = Flask(__name__)
    register_blueprints(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
