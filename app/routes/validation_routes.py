from flask import Blueprint, request

from app.middleware.auth_middleware import token_required
from app.services.validation_service import validate_multifactor
from app.utils.responses import success_response, error_response

validation_bp = Blueprint("validation", __name__)


@validation_bp.route("/multifactor", methods=["POST"])
@token_required
def multifactor():
    data = request.get_json()

    dni = request.current_user["dni"]

    success, message = validate_multifactor(
        dni=dni,
        face_valid=data.get("face_valid", False),
        fingerprint_valid=data.get("fingerprint_valid", False),
        dni_barcode_valid=data.get("dni_barcode_valid", False)
    )

    if not success:
        response, status = error_response(message, 400)
        return response, status

    response, status = success_response(message)
    return response, status