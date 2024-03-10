import pytest
import pytest_asyncio
from psycopg import AsyncConnection
from services.postgres import SchedulerPostgresService


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
    await conn.execute('drop database if exists scheduler_test')
    await conn.execute('create database scheduler_test')
    await conn.close()


@pytest_asyncio.fixture(scope='function', autouse=True)
async def test_sites(db_connection):
    await db_connection.execute("""
                        create table if not exists sites
                        (
                            id serial primary key,
                            url text not null unique,
                            regex text,
                            interval integer constraint sites_interval_check check (("interval" >= 5) AND ("interval" <= 300)),
                            next_check_at integer default 0 not null
                        )
                    """)
    await db_connection.execute('create index if not exists next_check_at_idx on sites (next_check_at)')

    await db_connection.execute("insert into sites (url, interval) values ('https://google.com', 7)")
    await db_connection.execute("""
                        insert into sites (url, interval, regex)
                        values ('https://aiven.io', 5, 'The trusted open source data platform for everyone')
                        """)
    yield
    await db_connection.execute('drop table if exists sites')


@pytest.fixture
def postgres_service(config):
    return SchedulerPostgresService(config.postgres)
