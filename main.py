from fastapi import FastAPI
from starlette.responses import JSONResponse
from core.conf import mail_conf
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.schemas import Ticket
from app.utils import get_template_context, check_token


app = FastAPI()

@app.post("/send_ticket")
async def sd_email(ticket: Ticket):
    if not check_token(ticket.autorization):
        return JSONResponse(
            status_code=401,
            content={'message': 'invalid token'}
        )
    template_context = get_template_context(ticket)
    message = MessageSchema(
        subject="Пересылка инцидента",
        recipients=['win1887@yandex.ru'],
        template_body=template_context,
        subtype=MessageType.html)
    fm = FastMail(mail_conf)
    try:
        await fm.send_message(message, template_name='email_template')
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'message': f'Ошибка при отправке письма {e}'}
        )
    return JSONResponse(status_code=200, content=template_context)
