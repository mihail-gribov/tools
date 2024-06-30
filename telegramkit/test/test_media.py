import pytest
from telegramkit.models import Media

class MockClient:
    pass

def test_media_get_html_photo():
    client = MockClient()
    media = Media(client, 1)
    media.url = 'https://example.com/photo.jpg'
    media.type = 'photo/jpg'
    assert media.get_html() == '<img src="https://example.com/photo.jpg" alt="photo">'
