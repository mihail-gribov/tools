import pytest
from bs4 import BeautifulSoup
from telegramkit.telegram_async import TelegramClient
from telegramkit.channel import Channel
from telegramkit.post import Post
from telegramkit.comment import Comment

# Импортируем HTML-ответы
from sample_responses import channel_html, post_html, post_html_no_views

class MockHttpClient:
    async def fetch(self, url: str, headers: dict = None) -> str:
        if "channel" in url:
            return channel_html
        elif "post" in url:
            return post_html
        return None

@pytest.fixture
def mock_http_client():
    return MockHttpClient()

@pytest.fixture
def telegram_client(mock_http_client):
    client = TelegramClient()
    client.http_client = mock_http_client
    return client

@pytest.mark.asyncio
async def test_fetch_html(telegram_client):
    url = "https://t.me/testchannel"
    html = await telegram_client.fetch_html(url)
    assert html is not None
    assert "Test Channel" in html

@pytest.mark.asyncio
async def test_get_channel(telegram_client):
    channel = await telegram_client.get_channel("testchannel")
    assert channel is not None
    assert channel.name == "Test Channel"
    assert channel.description == "Description"
    assert channel.subscribers == 1500

@pytest.mark.asyncio
async def test_load_posts(telegram_client):
    channel = await telegram_client.get_channel("testchannel")
    posts = await telegram_client.load_posts(channel)
    assert len(posts) > 0
    post = posts[1]
    assert post.html_content == '<div class="tgme_widget_message_text">Test post content</div>'
    assert post.views == 123

@pytest.mark.asyncio
async def test_get_post(telegram_client):
    post = await telegram_client.get_post("testchannel", 1)
    assert post is not None
    assert post.id == 1
    assert post.html_content == '<div class="tgme_widget_message_text">Test post content</div>'
    assert post.views == 123

@pytest.mark.asyncio
async def test_get_comments(telegram_client):
    channel = await telegram_client.get_channel("testchannel")
    post = Post(telegram_client, channel, 1)
    comments = await telegram_client.get_comments(post)
    assert comments is not None
    assert len(comments) > 0

@pytest.mark.asyncio
async def test_get_comment(telegram_client):
    channel = await telegram_client.get_channel("testchannel")
    post = Post(telegram_client, channel, 1)
    comment = await telegram_client.get_comment(post, 1)
    assert comment is not None
    assert comment.id == 1

if __name__ == "__main__":
    pytest.main()
