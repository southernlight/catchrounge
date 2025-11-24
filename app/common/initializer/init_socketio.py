from flask_socketio import SocketIO, join_room # join_room 추가
from flask import request                       # request 추가
import logging                                  # logging 추가
socketio = SocketIO(cors_allowed_origins="*")


def  _register_socket_handlers(socketio_instance):
    """
    주어진 SocketIO 인스턴스에 'connect' 이벤트 핸들러를 등록하고, 
    사용자의 username을 기반으로 Room에 가입시킵니다.
    """
    
    @socketio_instance.on('connect')
    def handle_connect():
        # 클라이언트가 연결 시 쿼리 파라미터로 전달한 username을 가져옵니다.
        username = request.args.get('username') 
        print("Socket connected for user:", username)
        if username:
            # 사용자의 username을 Room 이름으로 사용하여 join (가입)
            join_room(username) 
            logging.info(f"[Socket] User {username} connected and joined room {username}")
        else:
            logging.warning("[Socket] Unauthenticated user connected (no username provided).")

def init_socketio(app):
    socketio.init_app(app)
    _register_socket_handlers(socketio)
    return socketio