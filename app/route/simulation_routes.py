from flask import Blueprint,jsonify
import time
import math
import logging

simulation_bp = Blueprint('simulation_bp', __name__)

@simulation_bp.route("/api/simulate-cpu-load", methods=["GET"])
def simulate_cpu_load():
    """
    5초 동안 CPU를 집중적으로 사용하는 작업을 시뮬레이션합니다.
    이 작업은 Python GIL을 점유하여 다른 스레드(스케줄러 스레드 포함)의 실행을 방해합니다.
    """
    duration = 5  # CPU 부하를 지속할 시간 (초)
    start_time = time.time()
    
    # ⚠️ 중요한 로깅: 부하가 시작되었음을 기록합니다.
    logging.warning(f"Starting CPU load simulation for {duration} seconds.")
    
    count = 0
    # 5초 동안 CPU intensive loop 실행
    while time.time() - start_time < duration:
        # 복잡한 계산을 반복하여 CPU 점유율을 높입니다.
        # math.pow와 math.sqrt를 사용하여 부동 소수점 연산을 통해 CPU를 점유합니다.
        result = math.sqrt(math.pow(1234567, 2) + math.pow(9876543, 2)) / math.pi
        count += 1
    
    # ⚠️ 중요한 로깅: 부하가 끝났음을 기록합니다.
    logging.warning(f"CPU load simulation finished. Iterations: {count}")
    
    return jsonify({
        "status": "success",
        "message": f"CPU load finished after {duration} seconds. Check logs for scheduler status.",
        "iterations": count
    }), 200