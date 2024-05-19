from bs4 import BeautifulSoup
import markdownify
from .models import Channel, Post, Comment, Media, Author


def html_to_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def html_to_markdown(html_content: str) -> str:
    return markdownify.markdownify(html_content)


def parse_subscribers(subs_str: str) -> int:
    if 'K' in subs_str:
        return int(float(subs_str[:-1]) * 1000)
    elif 'M' in subs_str:
        return int(float(subs_str[:-1]) * 1000000)
    return int(subs_str)


def bs_to_author(msg: BeautifulSoup) -> Author:
    author_username = msg.find(class_='tgme_widget_message_user').find('a').get('href').split('/')[-1] if msg.find(class_='tgme_widget_message_user') else None
    author_photo = msg.find(class_='tgme_widget_message_user_photo').find('img').get('src') if msg.find(class_='tgme_widget_message_user_photo') else None
    return Author({
        'name': msg.find(class_='tgme_widget_message_author_name').text,
        'username': author_username,
        'photo': author_photo
    })


def bs_to_channel(bs: BeautifulSoup, name: str) -> Channel:
    info = bs.find(class_='tgme_channel_info')
    description = info.find(class_='tgme_channel_info_description').text if info.find(class_='tgme_channel_info_description') else None
    subscribers = parse_subscribers(info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text)
    picture = info.find(class_='tgme_page_photo_image').find('img').get('src') if info.find(class_='tgme_page_photo_image') else None
    return Channel({
        'url': f'https://t.me/{name}',
        'name': info.find(class_='tgme_channel_info_header_title').text,
        'description': description,
        'subscribers': subscribers,
        'picture': picture,
        'data': bs
    })


def bs_to_post(bs: BeautifulSoup, channel: Channel) -> Post:
    html_content = str(bs.find(class_='tgme_widget_message_text')).replace('<br/>', '\n') if bs.find(class_='tgme_widget_message_text') else None
    post_id = int(bs.get('data-post').split('/')[-1])
    views = parse_subscribers(bs.find(class_='tgme_widget_message_views').text) if bs.find(class_='tgme_widget_message_views') else 0
    media = [
        Media({'url': photo.get('style').split("background-image:url('")[1].split("')")[0], 'type': 'photo/jpg'}) 
        for photo in bs.find_all(class_='tgme_widget_message_photo_wrap')
    ] + [
        Media({'url': video.get('src'), 'type': 'video/mp4'}) 
        for video in bs.find_all(class_='tgme_widget_message_video')
    ] + [
        Media({'url': round_video.get('src'), 'type': 'round_video/mp4'}) 
        for round_video in bs.find_all(class_='tgme_widget_message_roundvideo')
    ] + [
        Media({'url': voice_msg.get('src'), 'type': 'voice/ogg'}) 
        for voice_msg in bs.find_all(class_='tgme_widget_message_voice')
    ]
    datetime = bs.find(class_='datetime').get('datetime') if bs.find(class_='datetime') else bs.find(class_='time').get('datetime')
    return Post({
        'channel': channel,
        'url': f'{channel.url}/{post_id}',
        'id': post_id,
        'html_content': html_content,
        'media': media,
        'views': views,
        'datetime': datetime,
        'data': bs
    })


def bs_to_comment(msg: BeautifulSoup, post: Post) -> Comment:
    reply = int(msg.find(class_='tgme_widget_message_reply').get('data-reply-to')) if msg.find(class_='tgme_widget_message_reply') else None
    return Comment({
        'post': post,
        'id': int(msg.get('data-post-id')),
        'html_content': str(msg.find(class_='js-message_text')).replace('<br/>', '\n'),
        'reply': reply,
        'author': bs_to_author(msg),
        'datetime': msg.find(class_='tgme_widget_message_date').find('time').get('datetime')
    })
