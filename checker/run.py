import asyncio
import logging
from asyncio import CancelledError

from app import CheckerApp
from config import CheckerConfig

from common.utils import setup_logging

logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    checker = CheckerApp(CheckerConfig())
    logger.info('Starting checker app')
    try:
        await checker.run()
    except (KeyboardInterrupt, CancelledError):
        logger.info('Stopping checker app')
        await checker.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
