from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.service.reservation_service import ReservationService
from app.service.table_service import TableService



def init_services(repositories, socketio, secret_key,db_client):

    auth_service = AuthService(repositories["user_repository"], secret_key)
    user_service = UserService(repositories["user_repository"])
    reservation_service = ReservationService(
        repositories["table_repository"],
        repositories["user_repository"],
        socketio,
        db_client
    )
    table_service = TableService(repositories["table_repository"])


    return {
        "auth_service": auth_service,
        "user_service": user_service,
        "reservation_service": reservation_service,
        "table_service": table_service
    }