from unittest.mock import AsyncMock

import pytest
from aiokafka.errors import KafkaTimeoutError

from common.models import Task


@pytest.mark.asyncio
async def test_send_task_method(kafka_service):
    task = Task(url='http://example.com', regex='example', valid_until=1234567890)
    await kafka_service.send_task(task)
    kafka_service._producer.send.assert_called_once_with(
        'site-check-tasks-test', {'url': 'http://example.com', 'regex': 'example', 'valid_until': 1234567890}
    )


@pytest.mark.asyncio
async def test_start_method(kafka_service):
    await kafka_service.start()
    kafka_service._producer.start.assert_called_once()


@pytest.mark.asyncio
async def test_stop_method(kafka_service):
    await kafka_service.stop()
    kafka_service._producer.stop.assert_called_once()


@pytest.mark.asyncio
async def test_send_task_method_exception_handling(kafka_service, caplog):
    kafka_service._producer.send = AsyncMock(side_effect=KafkaTimeoutError)
    task = Task(url='http://example.com', regex='example', valid_until=1234567890)
    await kafka_service.send_task(task)
    assert 'Kafka timed out while sending task' in caplog.text
