from flask import Blueprint, request

from app.services.auth_service import authenticate_user, generate_token
from app.utils.responses import success_response, error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    dni = data.get("dni")
    password = data.get("password")

    user = authenticate_user(dni, password)

    if not user:
        response, status = error_response("Credenciales inválidas", 401)
        return response, status

    token = generate_token(user)

    response, status = success_response("Login exitoso", {
        "token": token,
        "user": {
            "dni": user["dni"],
            "full_name": user["full_name"],
            "email": user["email"]
        }
    })

    return response, status