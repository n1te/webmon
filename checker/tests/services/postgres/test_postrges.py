import pytest


@pytest.mark.asyncio
async def test_save_metrics(postgres_service, db_connection, test_task_result):
    await postgres_service.save_metrics(test_task_result)
    cursor = await db_connection.execute("SELECT * FROM metrics WHERE url = 'http://example.com'")
    result = await cursor.fetchone()
    assert result == (1, 'http://example.com', 'example', 0.5, 200, True, None, 1234567890)


@pytest.mark.asyncio
async def test_save_metrics_error(broken_postgres_service, caplog):
    await broken_postgres_service.save_metrics(None)
    assert 'Postgres error while saving metrics' in caplog.text
