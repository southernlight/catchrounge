from datetime import datetime, timedelta,timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import time
from apscheduler.events import EVENT_JOB_SUBMITTED

import logging

log = logging.getLogger("my_app")


class ReservationService:
    
    def __init__(self,table_repository,user_repository,socketio, db_client):
        self.table_repository = table_repository
        self.user_repository = user_repository
        self.socketio = socketio

        executors = {
            'default' : ThreadPoolExecutor(10)
        }

        self.scheduler = BackgroundScheduler(executors=executors)

        self.scheduler.start()
        self.db_client = db_client

        self.last_heartbeat_time = None


        # 1. 🚨 [필수] Heartbeat 체크 작업 등록 (1초마다)
        # 이 작업이 1초마다 EVENT_JOB_SUBMITTED를 발생시켜 측정 기반을 만듭니다.
        self.scheduler.add_job(
            self.check_scheduler_interval, 
            'interval', 
            seconds=1, 
            id='heartbeat_check', # 이 ID로 이벤트를 추적합니다.
            replace_existing=True
        )

    def check_scheduler_interval(self):
            """1초마다 실행되는 Heartbeat 작업. 1초 초과 시 경고 로그를 남깁니다."""
            
            current_time = time.time()
            
            if self.last_heartbeat_time is not None:
                # 이전 실행 시간과의 실제 간격 계산
                interval = current_time - self.last_heartbeat_time
                
                # 1초를 초과했는지 확인합니다 (예: 1.1초 이상).
                if interval > 1.0: 
                    log.warning(
                        f"🚨 HEARTBEAT LAG WARNING! Expected ~1.0s, but saw {interval:.4f} seconds."
                    )
                else:
                    log.info(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] 💚 Heartbeat")

            
            # 현재 시간을 다음 비교를 위해 저장
            self.last_heartbeat_time = current_time

    # 🚨 워커 스레드를 점유할 긴 작업 추가
    def long_blocking_job(self, name):
        """실제 DB 쿼리나 네트워크 I/O처럼 오래 걸리는 작업을 시뮬레이션합니다."""
        log.info(f"[{datetime.now().strftime('%H:%M:%S')}] Job {name}: 🚨 워커 스레드 점유 시작 (10초 Block)")
        # CPU를 점유하기 위해 무한 루프와 시간 제한을 결합
        end_time = time.time() + 10 # 10초간 실행
        i = 0
        while time.time() < end_time:
            i += 1 # 실제 무거운 계산 시뮬레이션
        log.info(f"[{datetime.now().strftime('%H:%M:%S')}] Job {name}: ✅ 워커 스레드 반납")

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
        utc_end_time = (kst_now + timedelta(seconds=1)).astimezone(timezone.utc)

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

        run_date_for_long_jobs = datetime.now(timezone.utc) + timedelta(seconds=1)
        # self.scheduler.add_job(self.long_blocking_job, 'date', run_date=run_date_for_long_jobs, args=[f'LongJob-{1}'])
            
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

        # log.info(f"Expiring table {table_num} for user {username} at {datetime.now(timezone.utc).isoformat()}")
        """정확한 시간에 테이블 상태 업데이트"""

        table = self.table_repository.find_by_table_num(table_num)
        # log.info(f"Current table state: {table}") 
        # time.sleep(1.0)

        if not table["occupied"] or table["user_name"] != username:
            logging.info(f"Table {table_num} is already free or reserved by another user.")
            return

        # 테이블 상태 만료 처리
        self.table_repository.update_table(
            table_num,
            {"occupied": False,"user_name" : None ,"time": None}
        )
        # time.sleep(1.0)

        # 관련 사용자 정보 업데이트
        self.user_repository.update_user(
            username,
            {"is_reserved": 0}
        )
        # time.sleep(1.0)


        self.emit_table_update()
        self.emit_user_update(username)
        # time.sleep(1.0)

    
    def emit_table_update(self):
        tables = self.table_repository.find_all_tables()
        self.socketio.emit("table_update", {"tables": tables})

    def emit_user_update(self, username):
        user = self.user_repository.find_by_username(username)
        self.socketio.emit("user_update", {"user": user},room=username)

