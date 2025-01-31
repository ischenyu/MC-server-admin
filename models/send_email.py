import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template
import config

def send_email(email, captcha):
    """
    使用 Resend 的 SMTP 发送验证码邮件
    :param email: 收件人邮箱地址
    :param captcha: 验证码
    :param smtp_config: SMTP 配置字典，包含 host, port, username, password
    :param template_path: HTML模板文件路径
    :return: None
    """
    # 读取HTML模板
    with open('./models/template.html', "r", encoding="utf-8") as file:
        html_template = file.read()

    # 替换模板中的验证码
    template = Template(html_template)
    html_content = template.substitute(captcha=captcha)

    # 设置邮件内容
    msg = MIMEMultipart()
    msg["From"] = config.EMAIL_Config.FROM
    msg["To"] = email
    msg["Subject"] = "您的验证码"

    # 添加HTML内容
    msg.attach(MIMEText(html_content, "html"))

    # 连接SMTP服务器并发送邮件
    try:
        with smtplib.SMTP(config.EMAIL_Config.HOST, config.EMAIL_Config.PORT) as server:
            server.starttls()  # 启用TLS加密
            server.login(config.EMAIL_Config.USERNAME, config.EMAIL_Config.KEY)
            server.sendmail(msg["From"], email, msg.as_string())
        return True
    except Exception as e:
        return False
