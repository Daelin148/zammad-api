import os
import re

from dotenv import load_dotenv

from core.conf import zammad_client

from .schemas import Ticket

load_dotenv()


def get_articles_data(articles):
    articles_data = list()
    for article in articles:
        if article['internal'] == 'true':
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
    return articles_data


def get_template_context(ticket: Ticket):
    articles = zammad_client.ticket.articles(ticket.id)
    ticket_data = ticket.model_dump()
    articles = get_articles_data(articles)
    articles.sort(
        key=lambda article: int(article['id'])
    )
    ticket_data['description'] = articles.pop(0)['text']
    template_context = {
        'ticket': ticket_data,
        'articles': articles
    }
    return template_context


def check_token(token: str):
    return token == os.getenv('AUTH_TOKEN')
