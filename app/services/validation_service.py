from app.services.voter_service import mark_voter_as_validated


def validate_multifactor(dni, face_valid, fingerprint_valid, dni_barcode_valid):
    if not face_valid:
        return False, "Validación facial fallida"

    if not fingerprint_valid:
        return False, "Validación de huella fallida"

    if not dni_barcode_valid:
        return False, "Validación de código de barras del DNI fallida"

    updated = mark_voter_as_validated(dni)

    if not updated:
        return False, "Votante no encontrado"

    return True, "Validación multifactor completada"