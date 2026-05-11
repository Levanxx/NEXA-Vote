from flask import Blueprint

from app.services.voter_service import get_all_voters, get_voter_by_dni
from app.middleware.auth_middleware import token_required
from app.utils.responses import success_response, error_response

voter_bp = Blueprint("voter", __name__)


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