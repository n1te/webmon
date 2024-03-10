from unittest.mock import AsyncMock

import pytest
from services.kafka_producer import KafkaProducerConfig, KafkaProducerService


class TestKafkaProducerService(KafkaProducerService):
    def __init__(self, config: KafkaProducerConfig):
        self._producer = AsyncMock()
        self._topic = config.topic


@pytest.fixture
def kafka_service(config):
    return TestKafkaProducerService(config.kafka)
