from functools import wraps
from flask import request, current_app
import jwt

from app.utils.responses import error_response


def token_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            response, status = error_response("Token no proporcionado", 401)
            return response, status

        try:
            token = auth_header.split(" ")[1]

            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            request.current_user = payload

        except Exception:
            response, status = error_response("Token inválido o expirado", 401)
            return response, status

        return function(*args, **kwargs)

    return wrapper