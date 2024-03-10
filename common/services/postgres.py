import logging

from psycopg import AsyncConnection
from psycopg.conninfo import make_conninfo
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PostgresConfig(BaseModel):
    dbname: str
    user: str
    password: str | None = None
    port: int
    host: str

    @property
    def conn_info(self):
        return make_conninfo('', **dict(self))


class PostgresService:
    _conn_info: str
    _connection: AsyncConnection = None

    def __init__(self, config: PostgresConfig):
        self._conn_info = config.conn_info

    async def _get_connection(self):
        if self._connection is None:
            self._connection = await AsyncConnection.connect(self._conn_info)
        return self._connection

    async def close_connection(self):
        if self._connection is not None:
            await self._connection.close()
            logger.info('Connection closed')
