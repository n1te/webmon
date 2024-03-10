import asyncio

import pytest


@pytest.mark.asyncio
async def test_run_method(checker, valid_task, task_result, caplog):
    await checker.run()
    await asyncio.sleep(0.1)
    checker.http_service.check_site.assert_called_once_with(valid_task)
    checker.postgres_service.save_metrics.assert_called_once_with(task_result)
    assert 'Task for http://example.com?1 has expired'


@pytest.mark.asyncio
async def test_shutdown_method(checker):
    await checker.shutdown()
    checker.postgres_service.close_connection.assert_called_once()
