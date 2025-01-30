"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: Get Server Info.
"""

import json

import requests


def get_server_info():
    # Json
    try:
        data = requests.get('http://192.168.1.2:1233/system_info')
    except requests.exceptions.RequestException as e:
        return json.dumps({"success": False, "msg": str(e)})

    json_data = data.json()

    return json.dumps({"success": True, "data": json_data})
