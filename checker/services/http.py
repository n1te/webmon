import logging
import re
import time
from functools import lru_cache

from aiohttp import ClientError, ClientSession
from models import TaskResult
from pydantic import BaseModel

from common.models import Task

logger = logging.getLogger(__name__)


class HttpServiceConfig(BaseModel):
    timeout: int


class HTTPService:
    _timeout: int

    def __init__(self, config: HttpServiceConfig):
        self._timeout = config.timeout

    @staticmethod
    @lru_cache
    def _get_compiled_regex(regex: str) -> re.Pattern:
        """
        A little optimization, allowing to cache 128 recently used, compiled regular expressions
        """
        return re.compile(regex)

    async def check_site(self, task: Task) -> TaskResult:
        async with ClientSession() as session:
            start = time.monotonic()
            task_params = {
                'url': task.url,
                'regex': task.regex,
            }
            logger.info(f'Requesting {task.url}')
            try:
                resp = await session.get(task.url, timeout=self._timeout)
                task_params['http_code'] = resp.status
                text = await resp.text()
                task_params['response_time'] = time.monotonic() - start
            except ClientError as e:
                task_params['response_time'] = time.monotonic() - start
                task_params['error'] = f'Request error: {str(e)}'
                logger.exception(f'Error while requesting {task.url}')
            else:
                if task.regex:
                    pattern = self._get_compiled_regex(task.regex)
                    task_params['regex_match'] = bool(pattern.search(text))

        return TaskResult(**task_params)
