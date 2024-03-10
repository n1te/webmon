import pytest

from common.models import Task


@pytest.mark.asyncio
async def test_kafka_message(kafka_service_with_message):
    task = await anext(kafka_service_with_message.messages())
    assert isinstance(task, Task)
    assert task.url == f'http://example.com'
    assert task.regex == 'example'
    assert task.valid_until == 1234567890


@pytest.mark.asyncio
async def test_kafka_wrong_message(kafka_service_with_wrong_message, caplog):
    await anext(kafka_service_with_wrong_message.messages())
    assert 'Wrong message format' in caplog.text
