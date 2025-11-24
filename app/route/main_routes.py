from flask import Blueprint, render_template,g
from app.service.user_service import UserService
from app.service.table_service import TableService

main_bp = Blueprint('main_bp', __name__)

user_service = None
table_service = None

def init_main_routes(u_service: UserService, t_service: TableService):
    global user_service
    global table_service
    user_service = u_service
    table_service = t_service

@main_bp.route("/")
def home():
    username = g.user.get("username")
    user_info = user_service.get_user_info(username)
    tables_info = table_service.get_tables_info()
    tables_info = sorted(tables_info, key=lambda t: t["tableNum"])

    return render_template("main.html", user=user_info, tables=tables_info)