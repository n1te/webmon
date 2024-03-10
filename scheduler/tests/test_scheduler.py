import asyncio

import pytest

from common.models import Task


@pytest.mark.asyncio
async def test_run_method(scheduler):
    task = asyncio.create_task(scheduler.run())
    await asyncio.sleep(0.1)
    task.cancel()

    scheduler.kafka_service.send_task.assert_called_once_with(
        Task(url='http://example.com', regex='example', valid_until=1234567890)
    )


@pytest.mark.asyncio
async def test_shutdown_method(scheduler):
    await scheduler.shutdown()
    scheduler.postgres_service.close_connection.assert_called_once()
    scheduler.kafka_service.stop.assert_called_once()
