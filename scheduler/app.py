import asyncio
import logging

from config import SchedulerConfig
from models import Site
from services.kafka_producer import KafkaProducerService
from services.postgres import SchedulerPostgresService

from common.models import Task

logger = logging.getLogger(__name__)


class SchedulerApp:
    postgres_service: SchedulerPostgresService
    kafka_service: KafkaProducerService

    def __init__(self, config: SchedulerConfig):
        self.postgres_service = SchedulerPostgresService(config.postgres)
        self.kafka_service = KafkaProducerService(config.kafka)

    async def _send_task(self, site: Site):
        await self.kafka_service.send_task(Task(url=site.url, regex=site.regex, valid_until=site.next_check_at))

    async def run(self):
        await self.kafka_service.start()
        while True:
            logger.info('Fetching sites')
            async for site in self.postgres_service.get_sites_to_check():
                logger.info(f'Site for checking: {site}')
                asyncio.ensure_future(self._send_task(site))
            await asyncio.sleep(0.5)

    async def shutdown(self):
        await self.postgres_service.close_connection()
        await self.kafka_service.stop()
