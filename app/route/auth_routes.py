from flask import Blueprint, request, render_template,redirect,url_for,flash
from app.service.auth_service import AuthService

auth_bp = Blueprint('auth_bp', __name__)
auth_service = None

def init_auth_routes(service: AuthService):
    global auth_service
    auth_service = service

# ================== 회원가입 ==================
@auth_bp.route("/signup", methods=["GET"])
def show_signup():
    return render_template("signup.html")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    phone = request.form["phone"]

    success, message = auth_service.signup(username, password, phone)
    if success:
        flash("회원가입 성공! 로그인해주세요.", "success")
        return redirect(url_for("auth_bp.show_signin"))
    else:
        flash(message, "error")
        return redirect(url_for("auth_bp.show_signup"))
    

# ================== 로그인 ==================
@auth_bp.route("/signin", methods=["GET"])
def show_signin():
    return render_template("signin.html")

@auth_bp.route("/signin", methods=["POST"])
def signin():

    username = request.form["username"]
    password = request.form["password"]

    token = auth_service.signin(username, password)

    if token:
        response = redirect(url_for("main_bp.home"))
        response.set_cookie("accessToken", token, path="/")
        return response
    
    flash("로그인 실패. 아이디/비밀번호를 확인해주세요.", "error")
    return redirect(url_for("auth_bp.show_signin"))

# ================== 로그아웃 ==================
@auth_bp.route("/logout", methods=["GET"])
def logout():
    response = redirect(url_for("auth_bp.show_signin"))
    response.delete_cookie("accessToken", path="/")          
    return response