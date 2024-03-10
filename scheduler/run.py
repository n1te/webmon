import asyncio
import logging
from asyncio import CancelledError

from app import SchedulerApp
from config import SchedulerConfig

from common.utils import setup_logging

logger = logging.getLogger(__name__)


if __name__ == '__main__':

    async def main():
        setup_logging()
        scheduler = SchedulerApp(SchedulerConfig())
        logger.info('Starting scheduler app')
        try:
            await scheduler.run()
        except (CancelledError, KeyboardInterrupt):
            logger.info('Stopping scheduler app')
            await scheduler.shutdown()

    asyncio.run(main())
