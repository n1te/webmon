import asyncio
import logging
import time

from config import CheckerConfig
from services.http import HTTPService
from services.kafka_consumer import KafkaConsumerService
from services.postgres import CheckerPostgresService

from common.models import Task

logger = logging.getLogger(__name__)


class CheckerApp:
    kafka_service: KafkaConsumerService
    postgres_service: CheckerPostgresService
    http_service: HTTPService

    def __init__(self, config: CheckerConfig):
        self.kafka_service = KafkaConsumerService(config.kafka)
        self.postgres_service = CheckerPostgresService(config.postgres)
        self.http_service = HTTPService(config.http)

    async def _process_task(self, task: Task):
        if task.valid_until < int(time.time()):
            # Skipping all expired tasks
            logger.warning(f'Task for {task.url} has expired')
        else:
            task_result = await self.http_service.check_site(task)
            await self.postgres_service.save_metrics(task_result)

    async def run(self):
        async for task in self.kafka_service.messages():
            logger.info(f'Received task: {task}')
            asyncio.ensure_future(self._process_task(task))

    async def shutdown(self):
        await self.postgres_service.close_connection()
