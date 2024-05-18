import aiohttp
import bs4
from . import parsers
from .models import Channel, Post, Comment
from .__init__ import request_header

async def fetch_html(url: str) -> bs4.BeautifulSoup:
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=request_header) as resp:
            return bs4.BeautifulSoup(await resp.text('utf-8'), 'html.parser')

async def getChannel(url: str) -> Channel | None:
    name = url.replace('@', '').split('/')[-1]
    bs = await fetch_html(f'https://t.me/s/{name}')
    info = bs.find(class_='tgme_channel_info')
    return parsers.BStoChannel(bs, name) if info else None

async def getPost(channel: Channel | str, id: int) -> Post | None:
    if isinstance(channel, str):
        channel = await getChannel(channel)
    if not channel:
        return None

    bs = await fetch_html(f'https://t.me/{channel.url.split("/")[-1]}/{id}?embed=1')
    if bs.find(class_='tgme_widget_message_error'):
        return None
    return parsers.BStoPost(bs.find(class_='tgme_widget_message'), channel)

async def getComments(post: Post, limit: int = 10) -> list[Comment] | None:
    bs = await fetch_html(f'{post.url}?embed=1&discussion=1&comments_limit={limit}')
    if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
        return None
    comments = [parsers.BStoComments(msg, post) for msg in bs.findAll(class_='tgme_widget_message')]
    comments.reverse()
    return comments

async def getComment(post: Post, id: int) -> Comment | None:
    bs = await fetch_html(f'{post.url}?comment={id}&embed=1')
    if bs.find(class_='tgme_widget_message_error') or bs.find(class_='tme_no_messages_found'):
        return None
    return parsers.BStoComment(bs.findAll(class_='tgme_widget_message')[0], post)

async def getAllPosts(channel: Channel) -> list[Post]:
    posts = {}
    latest = await channel.getLatest()
    for p in latest:
        posts[p.id] = p

    while True:
        last_pid = sorted(posts.keys())[0]
        url = f'https://t.me/s/{channel.url.split("/")[-1]}/{last_pid}'
        bs = await fetch_html(url)
        for post in bs.findAll(class_='tgme_widget_message'):
            post_object = parsers.BStoPost(post, channel)
            posts[post_object.id] = post_object
        if 1 in posts:
            break

    return [posts[id] for id in sorted(posts.keys())]
