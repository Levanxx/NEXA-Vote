from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def home():
        return {
            "message": "NEXA Vote Back funcionando correctamente"
        }

    @app.route("/api/health")
    def health():
        return {
            "status": "ok",
            "service": "NEXA Vote Backend"
        }

    return app