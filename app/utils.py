import os
import re
from typing import Any

from dotenv import load_dotenv

from core.conf import zammad_client

from .schemas import Ticket

load_dotenv()


def get_articles_data(articles):
    articles_data = list()
    for article in articles:
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


def get_description_from_articles(articles: list[dict[str, Any]]):
    sorted_articles = sorted(
        articles,
        key=lambda article: int(article['id']),
        reverse=True
    )
    return sorted_articles.pop()['text']


def get_template_context(ticket: Ticket):
    articles = zammad_client.ticket.articles(ticket.id)
    ticket_data = ticket.model_dump()
    articles = get_articles_data(articles)
    ticket_data['description'] = get_description_from_articles(articles)
    template_context = {
        'ticket': ticket_data,
        'articles': articles
    }
    return template_context


def check_token(token: str):
    return token == os.getenv('AUTH_TOKEN')
