import time

from pydantic import BaseModel, Field


class TaskResult(BaseModel):
    url: str
    regex: str | None = None
    response_time: float
    http_code: int | None = None
    regex_match: bool | None = None
    error: str | None = None
    timestamp: int = Field(default_factory=lambda: int(time.time()))
