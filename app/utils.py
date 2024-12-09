import os
import re

from dotenv import load_dotenv
from starlette.responses import JSONResponse

from core.conf import zammad_client

from .schemas import Ticket

load_dotenv()


def get_articles_data(articles):
    articles_data = list()
    attachments = list()
    for article in articles:
        if article['internal']:
            continue
        articles_data.append(
            {
                'id': article['id'],
                'author': article['from'],
                'created_at': article['created_at'],
                'text': re.sub(
                    r'<[^>]+>',
                    '',
                    article['body'],
                    flags=re.S
                ),
            }
        )
        article_attachments = article['attachments']
        for attach in article_attachments:
            attachments.append((article['id'], attach))
    return articles_data, attachments


def download_attachments(ticket_id, attachments):
    serialized_attachments = list()
    for article_id, attachment in attachments:
        attachment_data = zammad_client.ticket_article_attachment.download(
            attachment['id'], article_id, ticket_id
        )
        attach = {
            'filename': attachment['filename'],
            'content': attachment_data,
            'type': attachment['preferences']['Content-Type']
        }
        serialized_attachments.append(attach)
    return serialized_attachments


def get_template_context(ticket: Ticket):
    try:
        articles = zammad_client.ticket.articles(ticket.id)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={'message': f'Ошибка при обращении к API Zammad: {e}'}
        )
    ticket_data = ticket.model_dump()
    articles, attachments = get_articles_data(articles)
    serialized_attachments = download_attachments(ticket.id, attachments)
    articles.sort(
        key=lambda article: int(article['id'])
    )
    ticket_data['description'] = articles.pop(0)['text']
    template_context = {
        'ticket': ticket_data,
        'articles': articles
    }
    return template_context, serialized_attachments


def check_token(token: str):
    return token == os.getenv('AUTH_TOKEN')
