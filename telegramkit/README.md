# TelegramKit

TelegramKit is a library for asynchronous interaction with Telegram channels and parsing data. It provides tools to fetch channel information, posts, comments, and more, all using asynchronous requests for efficient data handling.

## Features

- Fetch information about Telegram channels.
- Retrieve posts from channels.
- Get comments on posts.
- Convert post content to text, HTML, and Markdown formats.
- Extract links from post content.


# Usage
## Basic Example
Here's a basic example of how to use TelegramKit to fetch the latest messages from a Telegram channel:

```python
import asyncio
from telegramkit.telegram_async import getChannel

async def fetch_latest_messages(group_name: str, limit: int = 20):
    # Fetch channel information
    channel = await getChannel(f'@{group_name}')
    if not channel:
        print(f"Channel {group_name} not found or it is private.")
        return

    # Fetch the latest posts
    latest_posts = await channel.getLatest()
    for post in latest_posts[:limit]:
        print(f"Post ID: {post.id}")
        print("Text:")
        print(post.get_text())
        print("Markdown:")
        print(post.get_markdown())
        print("HTML:")
        print(post.html_content)
        print("Links:")
        print(post.getLinks())
        print("-----------")

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(fetch_latest_messages("@pythondaily"))
```
# Methods
**getChannel(url: str)** -> Channel | None
Fetches information about a Telegram channel.

**Channel.getLatest()** -> list[Post]
Retrieves the latest posts from the channel.

**Post.get_text()** -> str
Converts the post content to plain text.

**Post.get_markdown()** -> str
Converts the post content to Markdown format.

**Post.getLinks()** -> list
Extracts links from the post content.


# License
This project is licensed under the MIT License. See the LICENSE file for details.