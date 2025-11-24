from datetime import datetime, timedelta,timezone
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO)

class ReservationService:
    
    def __init__(self,table_repository,user_repository,socketio, db_client):
        self.table_repository = table_repository
        self.user_repository = user_repository
        self.socketio = socketio
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.db_client = db_client

    def _execute_reservation_logic(self, username, table_num, session):

        # 1. 사용자 정보 확인
        user = self.user_repository.find_by_username(username, session)
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다.")
        
        # 2. 사용자가 이미 예약한 테이블이 있는지 확인
        is_reserved = int(user.get("is_reserved", 0))
        if is_reserved > 0:
            raise ValueError("이미 예약하셨습니다.")

        # 3. 테이블 정보 확인
        table = self.table_repository.find_by_table_num(table_num, session)
        if table["occupied"]:
            raise ValueError("예약된 테이블입니다.")

        # 4. 예약 처리
        kst_now = datetime.now(timezone(timedelta(hours=9)))
        utc_end_time = (kst_now + timedelta(seconds=10)).astimezone(timezone.utc)

        # 5. 테이블 예약 상태 업데이트
        self.table_repository.update_table(
            table_num,
            {"occupied": True, "user_name": username, "time": utc_end_time.isoformat()},
            session
        )
 
        # 6. 사용자 예약 상태 업데이트
        self.user_repository.update_user(
            username,
            {"is_reserved": table_num},
            session
        )
            
        # 7. 예약 만료 작업 예약 (트랜잭션이 커밋된 후에도 스케줄러는 독립적으로 작동)
        self.schedule_expiration(table_num, username, utc_end_time)

        return {"result": "success", "message": "예약이 완료되었습니다."}

    def reserve_table(self, username, table_num):
        with self.db_client.start_session() as session:
            result = session.with_transaction(
                lambda s: self._execute_reservation_logic(username, table_num, s)
            )

            # 예약 완료 후 emit
            self.emit_table_update()
            self.emit_user_update(username)

            return result

    def cancel_table(self,username):

        user = self.user_repository.find_by_username(username)

        reserved_table_num = int(user.get("is_reserved", 0))

        if reserved_table_num == 0:
            raise ValueError("예약된 내용이 없습니다.")

        # 테이블 예약 취소 처리
        self.table_repository.update_table(
            reserved_table_num,
            {
                "occupied": False,
                "user_name": None,
                "time": None
            },
        )

        # 사용자 예약 상태 초기화
        self.user_repository.update_user(
            username,
            {"is_reserved": 0}
        )

         # 예약 취소 후 emit
        self.emit_table_update()
        # self.emit_user_update(username)

        return {"success": True, "message": f"테이블 {reserved_table_num} 예약이 취소되었습니다."} 
    
    def schedule_expiration(self, table_num, username, end_time):
        """예약 종료 시간을 기준으로 정확히 만료 작업 예약"""
        now = datetime.now(timezone.utc) 

        # 만료까지 남은 시간 계산
        time_remaining = end_time - now

        if time_remaining.total_seconds() > 0:
            # 만료 시간에 맞춰 작업 예약
            logging.info(f"time_remaining: {time_remaining.total_seconds()} seconds")
            logging.info(f"Scheduling expiration for table {table_num} at {end_time.isoformat()}")
            self.scheduler.add_job(self.expire_table, 'date', run_date=end_time, args=[table_num,username])

    def expire_table(self, table_num,username):

        logging.info(f"Expiring table {table_num} for user {username} at {datetime.now(timezone.utc).isoformat()}")
        """정확한 시간에 테이블 상태 업데이트"""

        table = self.table_repository.find_by_table_num(table_num)

        if not table["occupied"] or table["user_name"] != username:
            logging.info(f"Table {table_num} is already free or reserved by another user.")
            return

        # 테이블 상태 만료 처리
        self.table_repository.update_table(
            table_num,
            {"occupied": False,"user_name" : None ,"time": None}
        )
        # 관련 사용자 정보 업데이트
        self.user_repository.update_user(
            username,
            {"is_reserved": 0}
        )


        self.emit_table_update()
        self.emit_user_update(username)
    
    def emit_table_update(self):
        tables = self.table_repository.find_all_tables()
        self.socketio.emit("table_update", {"tables": tables})

    def emit_user_update(self, username):
        user = self.user_repository.find_by_username(username)
        self.socketio.emit("user_update", {"user": user},room=username)