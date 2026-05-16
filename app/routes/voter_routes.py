import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename

from app.services.voter_service import get_all_voters, get_voter_by_dni, register_voter
from app.middleware.auth_middleware import token_required
from app.utils.responses import success_response, error_response

voter_bp = Blueprint("voter", __name__)


def allowed_file(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


def save_uploaded_file(file, folder_name, dni):
    if not file:
        return None

    if file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    extension = filename.rsplit(".", 1)[1].lower()

    final_filename = f"{dni}_{folder_name}.{extension}"

    upload_folder = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        folder_name
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, final_filename)
    file.save(file_path)

    return file_path


@voter_bp.route("/register", methods=["POST"])
def create_voter():
    dni = request.form.get("dni")
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    password = request.form.get("password")
    birth_date = request.form.get("birth_date")

    required_fields = {
        "dni": dni,
        "full_name": full_name,
        "email": email,
        "password": password,
        "birth_date": birth_date
    }

    for field, value in required_fields.items():
        if not value:
            response, status = error_response(f"El campo {field} es requerido", 400)
            return response, status

    dni_photo = request.files.get("dni_photo")
    face_photo = request.files.get("face_photo")
    fingerprint_photo = request.files.get("fingerprint_photo")

    if not dni_photo:
        response, status = error_response("La foto del DNI es requerida", 400)
        return response, status

    if not face_photo:
        response, status = error_response("La foto del rostro es requerida", 400)
        return response, status

    if not fingerprint_photo:
        response, status = error_response("La imagen de huella es requerida", 400)
        return response, status

    dni_photo_path = save_uploaded_file(dni_photo, "dni", dni)
    face_photo_path = save_uploaded_file(face_photo, "face", dni)
    fingerprint_photo_path = save_uploaded_file(fingerprint_photo, "fingerprint", dni)

    if not dni_photo_path:
        response, status = error_response("Archivo de foto DNI inválido", 400)
        return response, status

    if not face_photo_path:
        response, status = error_response("Archivo de foto facial inválido", 400)
        return response, status

    if not fingerprint_photo_path:
        response, status = error_response("Archivo de huella inválido", 400)
        return response, status

    success, message = register_voter(
        dni=dni,
        full_name=full_name,
        email=email,
        password=password,
        birth_date=birth_date,
        dni_photo_path=dni_photo_path,
        face_photo_path=face_photo_path,
        fingerprint_photo_path=fingerprint_photo_path
    )

    if not success:
        response, status = error_response(message, 400)
        return response, status

    response, status = success_response(message, status_code=201)
    return response, status


@voter_bp.route("/", methods=["GET"])
@token_required
def list_voters():
    response, status = success_response("Votantes obtenidos", get_all_voters())
    return response, status


@voter_bp.route("/<dni>", methods=["GET"])
@token_required
def get_voter(dni):
    voter = get_voter_by_dni(dni)

    if not voter:
        response, status = error_response("Votante no encontrado", 404)
        return response, status

    voter.pop("password", None)

    response, status = success_response("Votante encontrado", voter)
    return response, status