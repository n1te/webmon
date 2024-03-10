from unittest.mock import AsyncMock

import psycopg
import pytest
import pytest_asyncio
from models import TaskResult
from psycopg import AsyncConnection
from services.postgres import CheckerPostgresService


@pytest_asyncio.fixture
async def db_connection(config) -> AsyncConnection:
    conn = await AsyncConnection.connect(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.postgres.host,
        port=config.postgres.port,
        dbname=config.postgres.dbname,
    )
    await conn.set_autocommit(True)
    yield conn
    await conn.close()


@pytest_asyncio.fixture(scope='module', autouse=True)
async def test_db(config):
    conn = await AsyncConnection.connect(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.postgres.host,
        port=config.postgres.port,
    )
    await conn.set_autocommit(True)
    await conn.execute('drop database if exists checker_test')
    await conn.execute('create database checker_test')
    await conn.close()


@pytest_asyncio.fixture(scope='function', autouse=True)
async def db_setup(db_connection):
    await db_connection.execute('drop table if exists metrics')
    await db_connection.execute("""
                create table metrics
                    (
                        id            serial  primary key,
                        url           text    not null,
                        regex         text,
                        response_time real    not null,
                        http_code     integer,
                        regex_match   boolean,
                        error         text,
                        timestamp     integer not null
                    )
            """)
    yield
    await db_connection.execute('drop table if exists metrics')


@pytest.fixture
def postgres_service(config):
    return CheckerPostgresService(config.postgres)


@pytest.fixture
def broken_postgres_service(postgres_service):
    postgres_service._get_connection = AsyncMock(side_effect=psycopg.Error)
    return postgres_service


@pytest.fixture
def test_task_result():
    return TaskResult(
        url='http://example.com',
        regex='example',
        response_time=0.5,
        http_code=200,
        regex_match=True,
        error=None,
        timestamp=1234567890,
    )
