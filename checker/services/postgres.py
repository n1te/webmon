import logging

import psycopg
from models import TaskResult

from common.services.postgres import PostgresService

logger = logging.getLogger(__name__)


class CheckerPostgresService(PostgresService):
    async def save_metrics(self, task_result: TaskResult):
        logger.info(f'Saving metrics: {task_result}')
        try:
            conn = await self._get_connection()
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO metrics (url, regex, response_time, http_code, regex_match, error, timestamp) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        task_result.url,
                        task_result.regex,
                        task_result.response_time,
                        task_result.http_code,
                        task_result.regex_match,
                        task_result.error,
                        task_result.timestamp,
                    ),
                )
                await conn.commit()
        except psycopg.Error:
            logger.exception('Postgres error while saving metrics')
