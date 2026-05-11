from flask import Blueprint

from app.middleware.auth_middleware import token_required
from app.services.vote_service import get_vote_summary
from app.utils.responses import success_response

report_bp = Blueprint("report", __name__)


@report_bp.route("/summary", methods=["GET"])
@token_required
def summary():
    response, status = success_response("Reporte generado", get_vote_summary())
    return response, status