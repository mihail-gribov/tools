import pytest
from telegramkit.models import Comment

class MockClient:
    pass

def test_comment_get_html():
    client = MockClient()
    comment = Comment(client, 1)
    comment.html_content = 'Test comment content'
    assert comment.get_html() == 'Test comment content'
