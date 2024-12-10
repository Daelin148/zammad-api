import os

from fastapi import FastAPI
from fastapi_mail import FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from dotenv import load_dotenv

from app.schemas import Ticket
from app.utils import check_token, get_template_context
from core.conf import mail_conf

load_dotenv()
app = FastAPI()


@app.post("/send_ticket")
async def sd_email(ticket: Ticket):
    if not check_token(ticket.autorization):
        return JSONResponse(
            status_code=401,
            content={'message': 'invalid token'}
        )
    template_context, attachments = get_template_context(ticket)
    message = MessageSchema(
        subject="Пересылка инцидента",
        recipients=[os.getenv('SD_MAIL')],
        template_body=template_context,
        subtype=MessageType.html,
        attachments=attachments
    )
    fm = FastMail(mail_conf)
    try:
        await fm.send_message(message, template_name='email_template.html')
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'message': f'Ошибка при отправке письма {e}'}
        )
    return JSONResponse(
        status_code=200,
        content={'message': 'Письмо успешно отправлено.'}
    )
