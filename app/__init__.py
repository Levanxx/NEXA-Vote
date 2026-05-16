from flask import Flask
from flask_cors import CORS

from app.config import Config

from app.routes.health_routes import health_bp
from app.routes.auth_routes import auth_bp
from app.routes.voter_routes import voter_bp
from app.routes.vote_routes import vote_bp
from app.routes.validation_routes import validation_bp
from app.routes.report_routes import report_bp
from app.routes.reconocimiento_routes import reconocimiento_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    # =========================
    # Blueprints
    # =========================

    app.register_blueprint(
        health_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        voter_bp,
        url_prefix="/api/voters"
    )

    app.register_blueprint(
        vote_bp,
        url_prefix="/api/votes"
    )

    app.register_blueprint(
        validation_bp,
        url_prefix="/api/validation"
    )

    app.register_blueprint(
        report_bp,
        url_prefix="/api/reports"
    )

    app.register_blueprint(
        reconocimiento_bp,
        url_prefix="/api/reconocimiento"
    )

    # =========================
    # Home Route
    # =========================

    @app.route("/")
    def home():
        return {
            "success": True,
            "message": "NEXA Vote Back funcionando correctamente"
        }, 200

    return app