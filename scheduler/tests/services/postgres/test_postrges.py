import time
from unittest.mock import AsyncMock

import psycopg
import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures('test_db', 'test_sites')
async def test_get_sites_to_check(postgres_service):
    sites = [s async for s in postgres_service.get_sites_to_check()]
    assert len(sites) == 2
    assert sites[0].id == 1
    assert sites[0].interval == 7
    assert sites[0].regex is None
    assert sites[0].url == 'https://google.com'
    assert sites[0].next_check_at >= int(time.time())

    assert sites[1].id == 2
    assert sites[1].interval == 5
    assert sites[1].regex == 'The trusted open source data platform for everyone'
    assert sites[1].url == 'https://aiven.io'

    assert len([s async for s in postgres_service.get_sites_to_check()]) == 0


@pytest.mark.asyncio
@pytest.mark.usefixtures('test_db', 'test_sites')
async def test_get_sites_to_check_error_handling(postgres_service, caplog):
    postgres_service._get_connection = AsyncMock(side_effect=psycopg.Error)
    assert len([s async for s in postgres_service.get_sites_to_check()]) == 0
    assert 'Error fetching sites to check' in caplog.text
