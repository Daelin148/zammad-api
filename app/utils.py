from core.conf import zammad_client
from .schemas import Ticket


def get_articles_data(articles):
    articles_data = list()
    for article in articles:
        articles_data.append(
            {
                'author': article['from'],
                'created_at': article['created_at'],
                'text': article['body'],
            }
        )
    return articles_data

def get_template_context(ticket: Ticket):
    articles = zammad_client.ticket.articles(ticket.id)
    template_context = {
        'ticket': ticket.model_dump(),
        'articles': get_articles_data(articles)
    }
    return template_context
    