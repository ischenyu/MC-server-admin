
import re
from flask import Blueprint, request, jsonify

from models import redisdb, mysql, send_email

register_url = Blueprint('register', __name__)

@register_url.route('/api/user/register', methods=['POST'])
def register():
    """

    :return:
    """
    try:
        data = request.get_json()
        username = data['username']
        email = data["email"]
        password = data["password"]
        captcha = data["captcha"]
        ip = request.headers.get('X-Forwarded-For')
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    if redisdb.verify_captcha(email, captcha) :
        if mysql.add_user(username, password, email, ip):
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400}), 400
    else:
        return jsonify({"code": 400, "message": "Captcha code is wrong"}), 400



@register_url.route('/api/user/register/get_captcha', methods=['GET'])
def get_captcha():
    """

    :return:
    """
    try:
        data = request.get_json()
        email = data["email"]
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)})
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        captcha = redisdb.captcha(email)
        send_email.send_email(email, captcha)
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400, "message": "邮箱不合法"}), 400
