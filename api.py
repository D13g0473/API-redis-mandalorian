from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import time

app = Flask(__name__)
CORS(app, origins=["http://localhost:9000"], allow_headers=["Content-Type"], methods=["GET", "POST"])

# Conexión a Redis
redis_client = redis.Redis(host="localhost", port=6378, db=0, decode_responses=True)

# Datos base: capítulos de The Mandalorian
chapters = {
    1: {"season": 1, "title": "Chapter 1   : The Mandalorian"},
    2: {"season": 1, "title": "Chapter 2   : The Child"},
    3: {"season": 1, "title": "Chapter 3   : The Sin"},
    4: {"season": 1, "title": "Chapter 4   : Sanctuary"},
    5: {"season": 1, "title": "Chapter 5   : The Gunslinger"},
    6: {"season": 1, "title": "Chapter 6   : The Prisoner"},
    7: {"season": 1, "title": "Chapter 7   : The Reckoning"},
    8: {"season": 1, "title": "Chapter 8   : Redemption"},
    9: {"season": 2, "title": "Chapter 9   : The Marshal"},
    10: {"season": 2, "title": "Chapter 10  : The Passenger"},
    11: {"season": 2, "title": "Chapter 11  : The Heiress"},
    12: {"season": 2, "title": "Chapter 12  : The Siege"},
    13: {"season": 2, "title": "Chapter 13  : The Jedi"},
    14: {"season": 2, "title": "Chapter 14  : The Tragedy"},
    15: {"season": 2, "title": "Chapter 15  : The Believer"},
    16: {"season": 2, "title": "Chapter 16  : The Rescue"},
    17: {"season": 3, "title": "Chapter 17  : The Apostate"},
    18: {"season": 3, "title": "Chapter 18  : The Mines of Mandalore"},
    19: {"season": 3, "title": "Chapter 19  : The Convert"},
    20: {"season": 3, "title": "Chapter 20  : The Foundling"},
    21: {"season": 3, "title": "Chapter 21  : The Pirate"},
    22: {"season": 3, "title": "Chapter 22  : Guns for Hire"},
    23: {"season": 3, "title": "Chapter 23  : The Spies"},
    24: {"season": 3, "title": "Chapter 24  : The Return"},
}

# Guardar capítulos base en Redis al iniciar si no existen
for chapter_id, data in chapters.items():
    redis_key = f"chapter:{chapter_id}"
    if not redis_client.exists(redis_key):
        redis_client.hset(redis_key, mapping=data)

# --------------------------
# FUNCIONES DE APOYO
# --------------------------

def get_chapter_status(chapter_id):
    """Devuelve el estado del capítulo basado en Redis (rented/reserved/available)."""
    if redis_client.exists(f"rented:{chapter_id}"):
        return "rented"
    elif redis_client.exists(f"reserved:{chapter_id}"):
        return "reserved"
    return "available"

# --------------------------
# RUTAS
# --------------------------

@app.route("/chapters", methods=["GET"])
def list_chapters():
    """Lista todos los capítulos con su estado dinámico."""
    chapters_list = []
    for key in redis_client.scan_iter("chapter:*"):
        chapter_data = redis_client.hgetall(key)
        chapter_id = int(key.split(":")[1])
        chapter_data["status"] = get_chapter_status(chapter_id)
        chapters_list.append({"id": chapter_id, **chapter_data})
    chapters_list.sort(key=lambda x: x["id"])
    return jsonify(chapters_list)

@app.route("/rent/<int:chapter_id>", methods=["POST"])
def rent_chapter(chapter_id):
    """Reserva un capítulo por 4 minutos."""
    if redis_client.exists(f"rented:{chapter_id}"):
        return jsonify({"error": f"Chapter {chapter_id} is already rented."}), 400
    if redis_client.exists(f"reserved:{chapter_id}"):
        return jsonify({"error": f"Chapter {chapter_id} is already reserved."}), 400

    redis_client.setex(f"reserved:{chapter_id}", 240, "reserved")
    return jsonify({"message": f"Chapter {chapter_id} reserved for 4 minutes."}), 200

@app.route("/confirm/<int:chapter_id>", methods=["POST"])
def confirm_payment(chapter_id):
    """Confirma el pago y alquila un capítulo por 24 horas."""
    data = request.get_json()
    price = data.get("price")

    if redis_client.exists(f"rented:{chapter_id}"):
        return jsonify({"error": f"Chapter {chapter_id} is already rented."}), 400
    if not redis_client.exists(f"reserved:{chapter_id}"):
        return jsonify({"error": f"Chapter {chapter_id} is not reserved."}), 400

    redis_client.delete(f"reserved:{chapter_id}")
    redis_client.setex(f"rented:{chapter_id}", 86400, "rented")
    return jsonify({"message": f"Payment confirmed. Chapter {chapter_id} rented for 24 hours at price {price}."}), 200

@app.route("/status", methods=["GET"])
def check_status():
    """Chequear estado de todos los capítulos."""
    status = {}
    for chapter_id in chapters:
        status[chapter_id] = get_chapter_status(chapter_id)
    return jsonify(status)

# --------------------------
# EJECUCIÓN
# --------------------------

if __name__ == "__main__":
    app.run(debug=True)
