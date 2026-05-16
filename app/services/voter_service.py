from datetime import date, datetime
from app.services.json_storage import read_json, write_json


def calculate_age(birth_date):
    birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
    today = date.today()

    age = today.year - birth.year

    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1

    return age


def register_voter(
    dni,
    full_name,
    email,
    password,
    birth_date,
    dni_photo_path,
    face_photo_path,
    fingerprint_photo_path
):
    voters = read_json("voters.json")

    existing_dni = next((voter for voter in voters if voter["dni"] == dni), None)

    if existing_dni:
        return False, "El DNI ya está registrado"

    existing_email = next((voter for voter in voters if voter["email"] == email), None)

    if existing_email:
        return False, "El correo ya está registrado"

    try:
        age = calculate_age(birth_date)
    except ValueError:
        return False, "Formato de fecha inválido. Use YYYY-MM-DD"

    if age < 18:
        return False, "El votante debe ser mayor de 18 años"

    new_voter = {
        "dni": dni,
        "full_name": full_name,
        "email": email,
        "password": password,
        "birth_date": birth_date,
        "age": age,
        "dni_photo_path": dni_photo_path,
        "face_photo_path": face_photo_path,
        "fingerprint_photo_path": fingerprint_photo_path,
        "has_voted": False,
        "multifactor_validated": False
    }

    voters.append(new_voter)
    write_json("voters.json", voters)

    return True, "Votante registrado correctamente"


def get_all_voters():
    voters = read_json("voters.json")

    return [
        {
            "dni": voter["dni"],
            "full_name": voter["full_name"],
            "email": voter["email"],
            "birth_date": voter.get("birth_date"),
            "age": voter.get("age"),
            "dni_photo_path": voter.get("dni_photo_path"),
            "face_photo_path": voter.get("face_photo_path"),
            "fingerprint_photo_path": voter.get("fingerprint_photo_path"),
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