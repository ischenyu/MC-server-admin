import redis
import secrets
import config

# 创建Redis连接池
pool = redis.ConnectionPool(
    host=config.REDIS_Config.HOST,
    port=config.REDIS_Config.PORT,
    password=config.REDIS_Config.PASSWORD,
    db=config.REDIS_Config.DB,
    decode_responses=True
)

# 创建Redis连接对象
conn = redis.Redis(connection_pool=pool)


def test_connection(conn):
    """
    测试Redis连接是否正常
    :param conn: Redis连接对象
    :return: True表示连接正常，False表示连接失败
    """
    try:
        conn.ping()
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False


def captcha(email):
    """
    生成验证码并存储到Redis中
    :param email: 用户邮箱，用于存储验证码
    :param conn: Redis连接对象
    :return: 生成的验证码
    :raises ConnectionError: 如果Redis连接失败
    """
    # 生成6位随机验证码
    captcha_code = secrets.randbelow(900000) + 100000
    if test_connection(conn):
        # 将验证码存储到Redis中，并设置超时时间
        conn.set(email, str(captcha_code), config.USER_MANAGE_Config.CAPTCHA_TIMEOUT_TIME)
        return str(captcha_code)
    else:
        raise ConnectionError("Connecting to redis failed!")


def verify_captcha(email, captcha):
    """
    验证用户输入的验证码是否正确
    :param email: 用户邮箱，用于从Redis中获取验证码
    :param captcha: 用户输入的验证码
    :return: True表示验证码正确，False表示验证码错误或已过期
    """
    # 从Redis中获取验证码
    result_captcha = conn.get(email)
    if result_captcha is None:
        return False
    try:
        # 比较用户输入的验证码和Redis中的验证码
        if result_captcha == str(captcha):
            conn.delete(email)
            return True
        else:
            return False
    except (TypeError, ValueError) as e:
        return False
