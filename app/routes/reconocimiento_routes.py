from flask import Blueprint, request, jsonify
import base64
import os
from datetime import datetime

reconocimiento_bp = Blueprint("reconocimiento_bp", __name__)

UPLOAD_FOLDER = "app/uploads/face"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@reconocimiento_bp.route("/facial", methods=["POST"])
def reconocimiento_facial():
    try:
        data = request.json

        imagen_base64 = data.get("imagen")

        if not imagen_base64:
            return jsonify({
                "success": False,
                "message": "No se recibió imagen"
            }), 400

        # Limpiar encabezado base64
        if "," in imagen_base64:
            imagen_base64 = imagen_base64.split(",")[1]

        imagen_bytes = base64.b64decode(imagen_base64)

        nombre_archivo = f"face_{datetime.now().timestamp()}.jpg"

        ruta_imagen = os.path.join(
            UPLOAD_FOLDER,
            nombre_archivo
        )

        with open(ruta_imagen, "wb") as f:
            f.write(imagen_bytes)

        return jsonify({
            "success": True,
            "message": "Reconocimiento facial exitoso",
            "file": nombre_archivo
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500