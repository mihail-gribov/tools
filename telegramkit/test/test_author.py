import pytest
from telegramkit.models import Author

class MockClient:
    pass

def test_author_get_html():
    client = MockClient()
    author = Author(client, 1)
    author.name = 'Test Author'
    author.username = 'testauthor'
    assert author.get_html() == '<div><h1>Test Author</h1><p>@testauthor</p></div>'
