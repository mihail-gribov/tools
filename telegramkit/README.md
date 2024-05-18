# TelegramKit

TelegramKit is a library for asynchronous interaction with Telegram channels and parsing data. It provides tools to fetch channel information, posts, comments, and more, all using asynchronous requests for efficient data handling.

## Features

- Fetch information about Telegram channels.
- Retrieve posts from channels.
- Get comments on posts.
- Convert post content to text, HTML, and Markdown formats.
- Extract links from post content.

# Telegram Kit

This project provides an asynchronous client to fetch and parse Telegram channel and post data using aiohttp and BeautifulSoup.

## Modules

### `config.py`

Contains configuration settings for the Telegram client, including user agent randomization.

### `http_client.py`

Defines the `HttpClient` class, which handles asynchronous HTTP requests.

### `models.py`

Defines the model classes representing Telegram entities.

- **Media**: Represents a media item with `url` and `type`.
- **Author**: Represents an author with `name`, `username`, and `photo`.
- **Comment**: Represents a comment with attributes like `post`, `id`, `text`, `reply`, `author`, and `datetime`.
- **Post**: Represents a post with attributes like `channel`, `url`, `id`, `html_content`, `media`, `views`, and `datetime`. Methods include fetching comments and converting HTML content to text or markdown.
- **Channel**: Represents a channel with attributes like `url`, `name`, `description`, `subscribers`, and `picture`. Methods include fetching posts and checking privacy status.

### `parsers.py`

Contains functions to parse HTML content into model objects.

- **parse_subscribers**: Converts a subscriber count string to an integer.
- **bs_to_author**: Converts a BeautifulSoup object to an `Author`.
- **bs_to_channel**: Converts a BeautifulSoup object to a `Channel`.
- **bs_to_post**: Converts a BeautifulSoup object to a `Post`.
- **bs_to_comments**: Converts a BeautifulSoup object to a list of `Comments`.
- **bs_to_comment**: Converts a BeautifulSoup object to a `Comment`.

### `telegram_async.py`

Provides asynchronous methods to interact with Telegram.

- **TelegramClient**: 
  - `fetch_html`: Fetches HTML content from a URL.
  - `get_channel`: Fetches and parses a channel's HTML page.
  - `get_post`: Fetches and parses a specific post's HTML page.
  - `get_comments`: Fetches and parses comments for a post.
  - `get_comment`: Fetches and parses a specific comment.
  - `get_all_posts`: Fetches all posts for a channel.

## Usage

### `main.py`

Example script to fetch the latest posts from a Telegram channel.

```python
import asyncio
from telegramkit.telegram_async import TelegramClient

async def fetch_latest_posts(group_name: str, limit: int = 10) -> None:
    client = TelegramClient()
    channel = await client.get_channel(f'@{group_name}')
    if not channel:
        print(f"Channel {group_name} not found or it is private.")
        return

    latest_posts = await channel.get_latest()
    latest_posts = latest_posts[:limit]

    for post in latest_posts:
        print(f"Post ID: {post.id}")
        print("Text:")
        print(post.get_text())
        print("-----------")

    await client.http_client.close()

if __name__ == "__main__":
    GROUP_NAME = "technodrifters"
    asyncio.run(fetch_latest_posts(GROUP_NAME))
