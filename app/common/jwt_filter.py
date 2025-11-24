from flask import request, g, redirect, url_for, jsonify
import jwt
from app.common.config import Config

# 인증이 필요 없는 엔드포인트 목록
PUBLIC_ENDPOINTS = {
    "auth_bp.show_signin",
    "auth_bp.signin",
    "auth_bp.show_signup",
    "auth_bp.signup",
    "simulation_bp.simulate_cpu_load",
    "static"
}


def jwt_filter():

    if request.endpoint in PUBLIC_ENDPOINTS:
        return

    token = request.cookies.get("accessToken")
    is_api = request.path.startswith("/api/")

    if not token:
        return handle_unauthorized(is_api)

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        g.user = payload
    except jwt.ExpiredSignatureError:
        return handle_unauthorized(is_api, "Token expired")
    except jwt.InvalidTokenError:
        return handle_unauthorized(is_api, "Invalid token")
    
def handle_unauthorized(is_api, message="Unauthorized"):
    if is_api:
        return jsonify({"error": message}), 401
    else:
        return redirect(url_for("auth_bp.show_signin"))