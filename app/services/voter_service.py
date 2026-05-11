from app.services.json_storage import read_json, write_json


def get_all_voters():
    voters = read_json("voters.json")

    return [
        {
            "dni": voter["dni"],
            "full_name": voter["full_name"],
            "email": voter["email"],
            "has_voted": voter["has_voted"],
            "multifactor_validated": voter["multifactor_validated"]
        }
        for voter in voters
    ]


def get_voter_by_dni(dni):
    voters = read_json("voters.json")

    return next((voter for voter in voters if voter["dni"] == dni), None)


def mark_voter_as_validated(dni):
    voters = read_json("voters.json")

    for voter in voters:
        if voter["dni"] == dni:
            voter["multifactor_validated"] = True
            write_json("voters.json", voters)
            return True

    return False


def mark_voter_as_voted(dni):
    voters = read_json("voters.json")

    for voter in voters:
        if voter["dni"] == dni:
            voter["has_voted"] = True
            write_json("voters.json", voters)
            return True

    return False