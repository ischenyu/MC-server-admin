"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: The user-login url.
"""

from flask import Blueprint, jsonify, request, redirect
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedSerializer  # 使用 TimedSerializer 替代
from models import mysql
import config

# 创建 Blueprint
login_url = Blueprint('login', __name__)

# 设置 Flask 应用的密钥（用于 token 加密）
login_url.secret_key = config.SERVER_Config.SECRET_KEY

# 初始化 Flask-HTTPAuth
auth = HTTPTokenAuth(scheme='Bearer')

# 生成 token 的函数
def generate_token(username):
    s = TimedSerializer(login_url.secret_key, expires_in=3600)  # token 有效期为 1 小时
    return s.dumps({'username': username})

# 验证 token 的函数
@auth.verify_token
def verify_token(token):
    s = TimedSerializer(login_url.secret_key)
    try:
        data = s.loads(token)
    except:
        return False
    return data['username']

# 登录路由
@login_url.route("/api/user/login/username", methods=["POST"])
def login():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e) + ' The request parameters are incomplete.'}), 500

    try:
        cookie = request.cookies.get("token")
        if cookie:
            return redirect('/')
    except Exception as e:
        pass
    try:
        username = data["user"]
        password = data["password"]
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e) + ' The request parameters are incomplete.'}), 500

    if mysql.login_username(username, password):  # mysql.login_username 是验证用户名和密码的函数
        token = generate_token(username)
        return jsonify({"code": 200, "token": token})
    else:
        return jsonify({"code": 401, "msg": "Invalid username or password"}), 401

# 受保护的路由示例
@login_url.route('/protected')
@auth.login_required
def protected():
    return jsonify({"code": 200, "msg": "You are authenticated!"})