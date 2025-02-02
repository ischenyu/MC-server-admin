"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: Function of connection to MySQL and password verification.
"""

import secrets
import datetime
import time
import hashlib
import logging
import pymysql
import config

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 数据库连接配置
DB_CONFIG = pymysql.connect(
    host=config.DB_Config.HOST,
    port=config.DB_Config.PORT,
    user=config.DB_Config.USER,
    passwd=config.DB_Config.PASSWORD,
    database=config.DB_Config.DB
)

def compute_hash(password, salt):
    """
    计算 AuthMe 的 SHA256 哈希值。

    :param password: 用户输入的密码（明文）
    :param salt: 盐值
    :return: 哈希值（格式：$SHA$<salt>$<hashed_password>）
    """
    # 第一次哈希：SHA256(password)
    first_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # 拼接第一次哈希结果和盐值
    combined = first_hash + salt

    # 第二次哈希：SHA256(combined)
    final_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()

    # 返回完整哈希值
    return f"$SHA${salt}${final_hash}"

def verify_password(input_password, stored_password):
    """
    验证用户输入的密码是否正确（基于 AuthMe 加密逻辑）。

    :param input_password: 用户输入的密码（明文）
    :param stored_password: 数据库中存储的密码（格式：$SHA$<salt>$<hashed_password>）
    :return: 如果密码正确返回 True，否则返回 False
    """
    try:
        # 去除首尾空格
        stored_password = stored_password.strip()
        input_password = input_password.strip()

        # 解析数据库中的密码
        parts = stored_password.split('$')
        if len(parts) != 4:
            raise ValueError("Invalid password format")

        algorithm = parts[1]  # 哈希算法（如 SHA）
        salt = parts[2]       # 盐值
        hashed_password = parts[3]  # 哈希值

        # 计算输入密码的哈希值
        input_hashed = compute_hash(input_password, salt)
        print(f"Input Hashed Password: {input_hashed}")

        # 比较哈希值
        return input_hashed == stored_password

    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

def login_username(username, input_password):
    """
    验证用户名和密码是否正确。

    :param username: 用户名
    :param input_password: 用户输入的密码（明文）
    :return: 如果验证成功返回 True，否则返回 False
    """
    try:
        # 使用上下文管理器管理数据库连接
        with DB_CONFIG.cursor() as cursor:
            # 查询数据库中的密码
            sql = "SELECT password FROM authme WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()

            if result is None:
                logger.info(f"登录失败: 用户名 {username} 不存在")
                return False

            stored_password = result[0]  # 获取数据库中存储的密码
            if verify_password(input_password, stored_password):
                logger.info(f"登录成功: 用户名 {username}")
                return True
            else:
                logger.info(f"登录失败: 用户名 {username} 或密码错误")
                return False

    except pymysql.MySQLError as e:
        logger.error(f"数据库错误: {e}")
        return False
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return False

def add_user(username, password, email, ip):
    """
    插入新用户到数据库。

    :param username: 用户名
    :param password: 用户密码（明文）
    :param email: 用户邮箱
    :return: 如果插入成功返回 True，否则返回 False
    """
    try:
        # 生成盐值
        salt = secrets.token_hex(16)
        time_stamp = int(datetime.datetime.now().timestamp() * 1000)
        # 第一次哈希：SHA256(password)
        first_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        # 拼接第一次哈希结果和盐值
        combined = first_hash + salt
        # 第二次哈希：SHA256(combined)
        final_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        # 返回完整哈希值
        hashed_password =  f"$SHA${salt}${final_hash}"

        # 使用上下文管理器管理数据库连接
        with DB_CONFIG.cursor() as cursor:
            # 插入用户到数据库
            sql = """
            INSERT INTO authme (username, realname, password, ip, lastlogin,x ,y, z,world, regdate, regip, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (username, username, hashed_password, ip, time_stamp, 0, 0, 0, 'world', time_stamp, ip, email))

        # 提交事务
        DB_CONFIG.commit()

        logger.info(f"用户 {username} 插入成功")
        return True

    except pymysql.MySQLError as e:
        logger.error(f"数据库错误: {e}")
        return False
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return False
