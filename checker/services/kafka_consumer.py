import asyncio
import json
import logging
from typing import AsyncIterable

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from pydantic import ValidationError

from common.models import Task
from common.services.kafka import KafkaConfig, KafkaServiceBase

logger = logging.getLogger(__name__)


class KafkaConsumerConfig(KafkaConfig):
    group_id: str


class KafkaConsumerService(KafkaServiceBase):
    _consumer = AIOKafkaConsumer

    def __init__(self, config: KafkaConsumerConfig):
        self._consumer = AIOKafkaConsumer(
            config.topic,
            bootstrap_servers=config.bootstrap_servers,
            group_id=config.group_id,
            value_deserializer=lambda v: json.loads(v),
            **self._get_ssl_params(config.ssl),
        )

    async def messages(self) -> AsyncIterable[Task]:
        while True:
            try:
                await self._consumer.start()
                try:
                    async for msg in self._consumer:
                        logger.info(f'Received message: {msg}')
                        try:
                            yield Task(**msg.value)
                        except ValidationError:
                            logger.exception(f'Wrong message format')
                finally:
                    await self._consumer.stop()
            except KafkaError:
                logger.exception('Error consuming messages')
                await asyncio.sleep(5)
                logger.info('Restarting consumer')
