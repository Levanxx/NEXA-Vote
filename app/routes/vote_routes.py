from flask import Blueprint, request

from app.middleware.auth_middleware import token_required
from app.services.vote_service import get_candidates, cast_vote
from app.utils.responses import success_response, error_response

vote_bp = Blueprint("vote", __name__)


@vote_bp.route("/candidates", methods=["GET"])
def candidates():
    response, status = success_response("Candidatos obtenidos", get_candidates())
    return response, status


@vote_bp.route("/cast", methods=["POST"])
@token_required
def vote():
    data = request.get_json()

    candidate_id = data.get("candidate_id")
    dni = request.current_user["dni"]

    success, message = cast_vote(dni, candidate_id)

    if not success:
        response, status = error_response(message, 400)
        return response, status

    response, status = success_response(message)
    return response, status