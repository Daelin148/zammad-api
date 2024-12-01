import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from fastapi_mail import ConnectionConfig
from zammad_py import ZammadAPI

load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
MAIL_PORT=587
MAIL_SERVER='mail.hprspc.com'
MAIL_FROM='sd_test@api-factory.ru'


zammad_client = ZammadAPI(
    url=os.getenv('ZAMMAD_URL'),
    username=os.getenv('ZAMMAD_USERNAME'),
    password=os.getenv('ZAMMAD_PASSWORD')
)


mail_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)
