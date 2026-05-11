from flask import Flask
from flask_cors import CORS
from app.routes.health_routes import health_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(health_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return {
            "message": "NEXA Vote Back funcionando correctamente"
        }

    return app