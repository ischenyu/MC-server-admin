

import redis
import random

from redis import RedisError

import config

poll = redis.ConnectionPool(
    host = config.REDIS_Config.HOST,
    port = config.REDIS_Config.PORT,
    password = config.REDIS_Config.PASSWORD,
    db = config.REDIS_Config.DB,
    decode_responses = True
)

conn = redis.Redis(connection_pool = poll)

def test_connection():   # 测试连接
    try:
        conn.ping()
        return True
    except Exception as e:
        return False

def captcha(email):
    """
    :param email: 用户邮箱，用于生成验证码
    :return captcha: 验证码
    :return:
    """
    captcha_code = random.randint(100000, 999999)
    if test_connection():
        conn.set(email, str(captcha_code), config.USER_MANAGE_Config.CAPTCHA_TIMEOUT_TIME)
        return str(captcha_code)
    else:
        conn.set(email, captcha_code)
    raise RedisError("Connecting to redis failed!")

def verify_captcha(email, captcha):
    """
    :param email:
    :param captcha:
    :return:
    """
    result_captcha = conn.get(email)
    if int(result_captcha) == int(captcha):
        return True
    else:
        return False

