from pydantic import BaseModel


class Task(BaseModel):
    url: str
    regex: str | None = None
    valid_until: int
