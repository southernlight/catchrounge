import logging


def init_logger(name="my_app", level=logging.INFO):
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 핸들러가 이미 붙어있으면 중복 방지
    if not logger.handlers:
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 포맷 설정
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
        )
        console_handler.setFormatter(formatter)

        # 핸들러 추가
        logger.addHandler(console_handler)
        
    logger.propagate = False

    # werkzeug 로그 끄기
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.disabled = True