from fastapi import FastAPI
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from starlette.responses import JSONResponse
from core.conf import mail_conf
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.schemas import Ticket
from app.utils import get_template_context


app = FastAPI()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
MAIL_PORT=587
MAIL_SERVER='mail.hprspc.com'
MAIL_FROM='sd_test@api-factory.ru'

message = MIMEMultipart("alternative")
message["Subject"], message["From"], message["To"] = "Тест HTML-письма", MAIL_FROM, "win1887@yandex.ru"
html = """<html><body><p>Привет, номер тикета 44.</p></body></html>"""
message.attach(MIMEText(html, "html"))


@app.post("/send_ticket")
async def sd_email(ticket: Ticket):
    
    # html = """<p>Привет! Номер тикета 44</p> """
    # message = MessageSchema(
    #     subject="Пересылка инцидента",
    #     recipients=['win1887@yandex.ru'],
    #     body=html,
    #     subtype=MessageType.html)
    # fm = FastMail(mail_conf)
    # await fm.send_message(message)
    
    try:
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(message)
        print("Письмо успешно отправлено")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
    template_context = get_template_context(ticket)
    return JSONResponse(status_code=200, content=template_context)
