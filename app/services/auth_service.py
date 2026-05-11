import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

from app.services.json_storage import read_json


def authenticate_user(dni, password):
    voters = read_json("voters.json")

    user = next((voter for voter in voters if voter["dni"] == dni), None)

    if not user:
        return None

    if user["password"] != password:
        return None

    return user


def generate_token(user):
    payload = {
        "dni": user["dni"],
        "full_name": user["full_name"],
        "exp": datetime.now(timezone.utc) + timedelta(
            hours=current_app.config["JWT_EXPIRES_HOURS"]
        )
    }

    return jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )