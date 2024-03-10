from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel
from services.kafka_consumer import KafkaConsumerConfig, KafkaConsumerService


class TestKafkaConsumerService(KafkaConsumerService):
    def __init__(self, config: KafkaConsumerConfig):
        self._consumer = AsyncMock()


@pytest.fixture
def kafka_service(config):
    return TestKafkaConsumerService(config.kafka)


class TestMessage(BaseModel):
    value: dict


async def msg_generator(*args):
    yield TestMessage(value={'url': 'http://example.com', 'regex': 'example', 'valid_until': 1234567890})


@pytest.fixture
def kafka_service_with_message(kafka_service):
    kafka_service._consumer = AsyncMock()
    kafka_service._consumer.__aiter__ = msg_generator
    return kafka_service


async def wrong_msg_generator(*args):
    yield TestMessage(value={'url': 'http://example.com'})
    # need to yield correct message to prevent infinite loop
    yield TestMessage(value={'url': 'http://example.com', 'regex': 'example', 'valid_until': 1234567890})


@pytest.fixture
def kafka_service_with_wrong_message(kafka_service):
    kafka_service._consumer = AsyncMock()
    kafka_service._consumer.__aiter__ = wrong_msg_generator
    return kafka_service
