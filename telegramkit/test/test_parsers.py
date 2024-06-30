import pytest
from bs4 import BeautifulSoup
from telegramkit.parsers import get_data_channel, get_data_posts

# Импортируем HTML-ответы
from sample_responses import channel_html, channel_html_no_description, post_html, post_html_no_views, post_html_no_text

def test_get_data_channel():
    soup = BeautifulSoup(channel_html, 'html.parser')
    data = get_data_channel(soup)
    
    assert data is not None
    assert data['name'] == 'Test Channel'
    assert data['description'] == 'Description'
    assert data['subscribers'] == 1500
    assert data['picture'] == 'https://example.com/picture.jpg'

def test_get_data_channel_no_description():
    soup = BeautifulSoup(channel_html_no_description, 'html.parser')
    data = get_data_channel(soup)
    
    assert data is not None
    assert data['name'] == 'Test Channel'
    assert data['description'] is None
    assert data['subscribers'] == 1500
    assert data['picture'] == 'https://example.com/picture.jpg'

def test_get_data_posts():
    soup = BeautifulSoup(post_html, 'html.parser')
    data_posts = get_data_posts(soup)
    
    assert data_posts is not None
    assert len(data_posts) == 1
    
    post = data_posts[0]
    assert post['id'] == 1
    assert post['html_content'] == '<div class="tgme_widget_message_text">Test post content</div>'
    assert post['views'] == 123
    assert post['datetime'] == '2022-01-01T12:00:00'

def test_get_data_posts_no_views():
    soup = BeautifulSoup(post_html_no_views, 'html.parser')
    data_posts = get_data_posts(soup)
    
    assert data_posts is not None
    assert len(data_posts) == 1
    
    post = data_posts[0]
    assert post['id'] == 1
    assert post['html_content'] == '<div class="tgme_widget_message_text">Test post content</div>'
    assert post['views'] == 0
    assert post['datetime'] == '2022-01-01T12:00:00'

def test_get_data_posts_no_text():
    soup = BeautifulSoup(post_html_no_text, 'html.parser')
    data_posts = get_data_posts(soup)
    
    assert data_posts is not None
    assert len(data_posts) == 1
    
    post = data_posts[0]
    assert post['id'] == 1
    assert post['html_content'] is None
    assert post['views'] == 123
    assert post['datetime'] == '2022-01-01T12:00:00'

if __name__ == "__main__":
    pytest.main()
