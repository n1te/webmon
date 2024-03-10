import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock_site_request')
async def test_http_check_site_success(http_service, valid_task):
    result = await http_service.check_site(valid_task)
    assert result.url == valid_task.url
    assert result.regex == valid_task.regex
    assert result.regex_match
    assert result.http_code == 200
    assert result.response_time > 0
    assert result.error is None


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock_site_request')
async def test_http_check_site_regex_failure(http_service, valid_task):
    valid_task.regex = 'invalid regex'
    result = await http_service.check_site(valid_task)
    assert not result.regex_match


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock_site_request_fail')
async def test_http_check_site_failure(http_service, valid_task):
    result = await http_service.check_site(valid_task)
    assert result.error == 'Request error: some error'
