from flask import Flask
from app.common.config import Config
from app.common.initializer.init_db import init_db, init_tables,get_db_client
from app.common.initializer.init_socketio import init_socketio
from app.common.initializer.init_repositories import init_repositories
from app.common.initializer.init_services import init_services
from app.common.initializer.init_blueprints import init_blueprints
from app.common.jwt_filter import jwt_filter
from app.common.error_handler import register_error_handlers

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # DB 초기화
    db = init_db(app)
    init_tables(db)

    # SocketIO 초기화
    socketio = init_socketio(app)

    # Repository
    repositories = init_repositories(db)

    # Service 초기화
    services = init_services(repositories, socketio, app.config["SECRET_KEY"],get_db_client())

    # Blueprint 등록
    init_blueprints(app, services)

    # JWT 필터 등록
    app.before_request(jwt_filter)

    # 에러 핸들러 등록
    register_error_handlers(app)

    return app, socketio