"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: The main program entry.
"""

import json

from flask import Blueprint, jsonify

from models import get_server_info

basic_url = Blueprint('basic', __name__)

@basic_url.route("/api/server_info", methods=['GET'])
def server_info():
    data = get_server_info.get_server_info()
    if json.loads(data)['success']:
        return jsonify({"code": 200, "data": data})
    else:
        return jsonify({"code": 500, "msg": data}), 500
