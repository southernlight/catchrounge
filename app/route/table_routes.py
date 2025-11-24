from flask import Blueprint,g,request
from app.service.table_service import TableService

table_bp = Blueprint('table_bp', __name__)
table_service : TableService = None

def init_table_routes(t_service: TableService):
    global table_service
    table_service = t_service

@table_bp.route("/api/tables/<int:table_num>", methods=["GET"])
def get_table_info(table_num):
    table = table_service.get_table_info(table_num)
    if not table:
        return {"success": False, "message": "Table not found"}, 404
    return {"success": True, "table": table}