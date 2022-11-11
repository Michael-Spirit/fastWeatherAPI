import pytest


@pytest.mark.asyncio
async def test_metrics(client):
    response = await client.get(client.app.url_path_for('metrics'))

    assert 200 == response.status_code, response.text
