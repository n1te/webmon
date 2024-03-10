from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from app import SchedulerApp
from config import SchedulerConfig
from models import Site


@pytest.fixture(scope='session')
def config():
    c = SchedulerConfig()
    c.postgres.dbname = 'scheduler_test'
    c.kafka.topic = 'site-check-tasks-test'
    return c


async def sites_async_generator():
    yield Site(
        id=1,
        url='http://example.com',
        regex='example',
        interval=5,
        next_check_at=1234567890,
    )


@pytest_asyncio.fixture
async def scheduler(config):
    app = SchedulerApp(config)
    app.postgres_service = AsyncMock()
    app.postgres_service.get_sites_to_check = sites_async_generator
    app.kafka_service = AsyncMock()
    return app
