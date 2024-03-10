from pydantic import BaseModel


class Site(BaseModel):
    id: int
    url: str
    regex: str | None = None
    interval: int
    next_check_at: int
