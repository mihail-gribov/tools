import pytest
from typing import Optional
from telegramkit.channel import Channel

class MockClient:
    async def load_posts(self, channel, post_id=None):
        return {1: 'post1', 2: 'post2'}

@pytest.mark.asyncio
async def test_channel_get_last_post():
    client = MockClient()
    channel = Channel(client, 'testchannel')
    last_post = await channel.get_last_post()
    assert last_post == 'post2'

@pytest.mark.asyncio
async def test_channel_get_post():
    client = MockClient()
    channel = Channel(client, 'testchannel')
    post = await channel.get_post(1)
    assert post == 'post1'
