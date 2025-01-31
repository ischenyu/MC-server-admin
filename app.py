"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: The main program entry.
"""

from flask import Flask

from api.basic import basic_url
from api.user.login import login_url
from api.user.register import register_url

app = Flask(__name__)
app.register_blueprint(login_url)
app.register_blueprint(basic_url)
app.register_blueprint(register_url)
