import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from zammad_py import ZammadAPI

load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_FROM = os.getenv('MAIL_FROM')


zammad_client = ZammadAPI(
    url=os.getenv('ZAMMAD_URL'),
    username=os.getenv('ZAMMAD_USERNAME'),
    password=os.getenv('ZAMMAD_PASSWORD'),
    http_token=os.getenv('ZAMMAD_API_TOKEN')
)
mail_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
)
