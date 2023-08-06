import binancechain

import pytest


@pytest.fixture
async def client():
    client = binancechain.HTTPClient(testnet=True)
    yield client
    await client.close()



@pytest.mark.asyncio
async def test_async_with(client):
    async with binancechain.HTTPClient() as client:
        time = await client.get_time()
        print(time)

"""

@pytest.mark.asyncio
async def test_async_for(client):
    async with binancechain.WebSocket() as ws:
        ws.subscribe_all_tickers()
        async for msg in ws:
            print(msg)
"""
