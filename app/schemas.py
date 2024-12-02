from pydantic import BaseModel


class Ticket(BaseModel):
    autorization: str
    id: int
    number: int
    author: str
    created_at: str
    title: str