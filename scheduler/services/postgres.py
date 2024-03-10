import logging
import time
from typing import AsyncIterable

import psycopg
from models import Site

from common.services.postgres import PostgresService

logger = logging.getLogger(__name__)


class SchedulerPostgresService(PostgresService):
    async def get_sites_to_check(self) -> AsyncIterable[Site]:
        try:
            conn = await self._get_connection()
            async with conn.cursor() as cur:
                now = int(time.time())
                await cur.execute(
                    """
                    UPDATE sites 
                    SET next_check_at = EXTRACT(EPOCH FROM NOW()) + interval
                    WHERE next_check_at <= %s 
                    RETURNING id, url, regex, interval, next_check_at
                    """,
                    (now,),
                )
                await conn.commit()
                async for record in cur:
                    yield Site(
                        id=record[0],
                        url=record[1],
                        regex=record[2],
                        interval=record[3],
                        next_check_at=record[4],
                    )
        except psycopg.Error:
            logger.exception('Error fetching sites to check')
