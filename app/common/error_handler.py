from flask import jsonify, current_app

def register_error_handlers(app):
    """
    Flask 앱에 공통 errorhandler 등록
    """

    # -------------------------
    # 클라이언트 요청 문제
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = jsonify({
            "result": "fail",
            "message": str(error)
        })
        response.status_code = 400
        return response

    # -------------------------
    # 그 외 모든 서버 예외
    @app.errorhandler(Exception)
    def handle_exception(error):
        current_app.logger.error(f"Internal server error: {error}")
        response = jsonify({
            "result": "fail",
            "message": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        })
        response.status_code = 500
        return response
