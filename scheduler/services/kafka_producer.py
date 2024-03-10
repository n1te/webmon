import json
import logging

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError

from common.models import Task
from common.services.kafka import KafkaConfig, KafkaServiceBase

logger = logging.getLogger(__name__)


class KafkaProducerConfig(KafkaConfig):
    request_timeout_ms: int = 5000


class KafkaProducerService(KafkaServiceBase):
    _producer: AIOKafkaProducer
    _topic: str

    def __init__(self, config: KafkaProducerConfig):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=config.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode(),
            compression_type='gzip',
            request_timeout_ms=config.request_timeout_ms,
            **self._get_ssl_params(config.ssl),
        )
        self._topic = config.topic

    async def start(self):
        await self._producer.start()

    async def send_task(self, task: Task):
        try:
            await self._producer.send(self._topic, dict(task))
        except KafkaTimeoutError:
            logger.warning(f'Kafka timed out while sending task {task}')
        else:
            logger.info(f'Sent task: {task}')

    async def stop(self):
        await self._producer.stop()
        logger.info('Kafka producer stopped')
