import time
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from app import CheckerApp
from config import CheckerConfig
from models import TaskResult

from common.models import Task


@pytest.fixture(scope='session')
def config():
    c = CheckerConfig()
    c.postgres.dbname = 'checker_test'
    return c


@pytest.fixture
def valid_task():
    return Task(url='http://example.com', regex='example', valid_until=int(time.time()) + 60)


@pytest.fixture
def expired_task():
    return Task(url='http://example.com?1', regex='example2', valid_until=0)


@pytest.fixture
def task_result():
    return TaskResult(
        url='http://example.com',
        regex='example',
        response_time=0.5,
        http_code=200,
        regex_match=True,
        error=None,
        timestamp=int(time.time()),
    )


@pytest.fixture
def tasks_async_generator(valid_task, expired_task):
    async def generator():
        yield valid_task
        yield expired_task

    return generator


@pytest_asyncio.fixture
async def checker(config, tasks_async_generator, task_result):
    app = CheckerApp(config)
    app.postgres_service = AsyncMock()
    app.kafka_service = AsyncMock()
    app.kafka_service.messages = tasks_async_generator
    app.http_service = AsyncMock()
    app.http_service.check_site = AsyncMock(return_value=task_result)
    return app
