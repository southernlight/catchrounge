from flask import Blueprint,g,request,jsonify
from app.service.reservation_service import ReservationService


reservation_bp = Blueprint('reservation_bp', __name__)

reservation_service : ReservationService = None

def init_reservation_routes(r_service: ReservationService):
    global reservation_service
    reservation_service = r_service

@reservation_bp.route("/api/tables/me", methods=["PUT"])
def reserve_table():
    username = g.user.get("username")
    table_num = request.get_json().get("tableNum")

    result , code = reservation_service.reserve_table(username, int(table_num))
    
    return jsonify(result), code

@reservation_bp.route("/api/tables/me", methods=["DELETE"])
def cancel_table():
    username = g.user.get("username")

    success, message = reservation_service.cancel_table(username)

    return {"success": success, "message": message}

