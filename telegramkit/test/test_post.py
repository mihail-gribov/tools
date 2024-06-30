import pytest
from telegramkit.models import Post, Channel

class MockClient:
    async def load_posts(self, channel, post_id=None):
        return {}

class MockChannel(Channel):
    async def get_post(self, post_id):
        return Post(self.client, self, post_id)

@pytest.mark.asyncio
async def test_post_prior():
    client = MockClient()
    channel = MockChannel(client, 'testchannel')
    post = Post(client, channel, 1)
    prior_post = await post.prior()
    assert prior_post.id == 0

@pytest.mark.asyncio
async def test_post_next():
    client = MockClient()
    channel = MockChannel(client, 'testchannel')
    post = Post(client, channel, 1)
    next_post = await post.next()
    assert next_post.id == 2
