from pydantic import BaseModel


class Ticket(BaseModel):
    id: int
    number: int
    author: str
    created_at: str
    title: str