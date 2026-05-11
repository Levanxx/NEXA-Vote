from datetime import datetime, timezone

from app.services.json_storage import read_json, write_json
from app.services.voter_service import get_voter_by_dni, mark_voter_as_voted


def get_candidates():
    return read_json("candidates.json")


def cast_vote(dni, candidate_id):
    voter = get_voter_by_dni(dni)

    if not voter:
        return False, "Votante no encontrado"

    if not voter["multifactor_validated"]:
        return False, "Primero debe completar la validación multifactor"

    if voter["has_voted"]:
        return False, "El votante ya emitió su voto"

    candidates = read_json("candidates.json")
    candidate = next((c for c in candidates if c["id"] == candidate_id), None)

    if not candidate:
        return False, "Candidato no encontrado"

    votes = read_json("votes.json")

    votes.append({
        "id": len(votes) + 1,
        "candidate_id": candidate_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    })

    write_json("votes.json", votes)
    mark_voter_as_voted(dni)

    return True, "Voto registrado correctamente"


def get_vote_summary():
    candidates = read_json("candidates.json")
    votes = read_json("votes.json")
    voters = read_json("voters.json")

    results = []

    for candidate in candidates:
        total = len([vote for vote in votes if vote["candidate_id"] == candidate["id"]])

        results.append({
            "candidate": candidate["name"],
            "party": candidate["party"],
            "total_votes": total
        })

    return {
        "total_voters": len(voters),
        "total_votes": len(votes),
        "participation_percentage": round((len(votes) / len(voters)) * 100, 2),
        "results": results
    }