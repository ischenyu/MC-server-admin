"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: Function of connecton Mysql.
"""
import base64
import hashlib
import logger
import pymysql
import logging

import config

DB_CONFIG = pymysql.connect(
    host = config.DB_Config.HOST,
    port = config.DB_Config.PORT,
    user = config.DB_Config.USER,
    passwd = config.DB_Config.PASSWORD,
    database = config.DB_Config.DB
)
# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def verify_password(input_password, stored_password):
    """
    验证用户输入的密码是否正确。

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
        if len(parts) != 4 or parts[1] != 'SHA':
            raise ValueError("Invalid password format")

        algorithm = parts[1]  # SHA
        salt = parts[2]       # 盐值
        hashed_password = parts[3]  # 哈希值

        print(f"Salt: {salt}")
        print(f"Stored Hashed Password: {hashed_password}")

        # 尝试不同的加盐方式和编码
        salt_bytes = salt.encode('utf-8')
        input_password_bytes = input_password.encode('utf-8')

        # 方式 1：salt + password (SHA-256 + Hex)
        input_hashed_1 = hashlib.sha256(salt_bytes + input_password_bytes).hexdigest()
        print(f"Input Hashed (salt + password, SHA-256 + Hex): {input_hashed_1}")

        # 方式 2：salt + password (SHA-256 + Base64)
        hash_bytes_2 = hashlib.sha256(salt_bytes + input_password_bytes).digest()
        input_hashed_2 = base64.b64encode(hash_bytes_2).decode('utf-8')
        print(f"Input Hashed (salt + password, SHA-256 + Base64): {input_hashed_2}")

        # 方式 3：password + salt (SHA-256 + Hex)
        input_hashed_3 = hashlib.sha256(input_password_bytes + salt_bytes).hexdigest()
        print(f"Input Hashed (password + salt, SHA-256 + Hex): {input_hashed_3}")

        # 方式 4：password + salt (SHA-256 + Base64)
        hash_bytes_4 = hashlib.sha256(input_password_bytes + salt_bytes).digest()
        input_hashed_4 = base64.b64encode(hash_bytes_4).decode('utf-8')
        print(f"Input Hashed (password + salt, SHA-256 + Base64): {input_hashed_4}")

        # 比较哈希值
        if input_hashed_1 == hashed_password:
            return True
        elif input_hashed_2 == hashed_password:
            return True
        elif input_hashed_3 == hashed_password:
            return True
        elif input_hashed_4 == hashed_password:
            return True
        else:
            return False

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
