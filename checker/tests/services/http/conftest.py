import pytest
from aiohttp import ClientError
from aioresponses import aioresponses
from services.http import HTTPService


@pytest.fixture
def mock_site_request(valid_task):
    with aioresponses() as mock:
        mock.get(valid_task.url, status=200, body='example content')
        yield


@pytest.fixture
def mock_site_request_fail(valid_task):
    with aioresponses() as mock:
        mock.get(valid_task.url, exception=ClientError('some error'))
        yield


@pytest.fixture
def http_service(config):
    return HTTPService(config.http)
