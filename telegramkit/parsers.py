from .models import Channel, Post, Comment, Media, Author
import bs4

def parse_subscribers(subs_str: str) -> int:
    if 'K' in subs_str:
        return int(float(subs_str[:-1]) * 1000)
    elif 'M' in subs_str:
        return int(float(subs_str[:-1]) * 1000000)
    return int(subs_str)

def BStoChannel(bs, name) -> Channel:
    info = bs.find(class_='tgme_channel_info')
    description = info.find(class_='tgme_channel_info_description').text if info.find(class_='tgme_channel_info_description') else None
    subscribers = parse_subscribers(info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text)
    picture = info.find(class_='tgme_page_photo_image').find('img').get('src') if info.find(class_='tgme_page_photo_image') else None
    return Channel(f'https://t.me/{name}', info.find(class_='tgme_channel_info_header_title').text, description, subscribers, picture, bs)

def BStoPost(bs, channel) -> Post:
    html_content = str(bs.find(class_='tgme_widget_message_text')).replace('<br/>', '\n') if bs.find(class_='tgme_widget_message_text') else None
    id = int(bs.get('data-post').split('/')[-1])
    views = parse_subscribers(bs.find(class_='tgme_widget_message_views').text) if bs.find(class_='tgme_widget_message_views') else 0
    media = [Media(photo.get('style').split("background-image:url('")[1].split("')")[0], 'photo/jpg') for photo in bs.findAll(class_='tgme_widget_message_photo_wrap')] + \
            [Media(video.get('src'), 'video/mp4') for video in bs.findAll(class_='tgme_widget_message_video')] + \
            [Media(roundvideo.get('src'), 'round_video/mp4') for roundvideo in bs.findAll(class_='tgme_widget_message_roundvideo')] + \
            [Media(voicemsg.get('src'), 'voice/ogg') for voicemsg in bs.findAll(class_='tgme_widget_message_voice')]
    datetime = bs.find(class_='datetime').get('datetime') if bs.find(class_='datetime') else bs.find(class_='time').get('datetime')
    return Post(channel, f'{channel.url}/{id}', id, html_content, media, views, datetime, bs)

def BStoComments(msg, post) -> Comment:
    reply = int(msg.find(class_='tgme_widget_message_reply').get('data-reply-to')) if msg.find(class_='tgme_widget_message_reply') else None
    return Comment(
        post, 
        int(msg.get('data-post-id')), 
        bs4.BeautifulSoup(str(msg.find(class_='js-message_text')).replace('<br/>', '\n'), 'html.parser').text, 
        reply, 
        BStoAuthor(msg), 
        msg.find(class_='tgme_widget_message_date').find('time').get('datetime')
    )

def BStoComment(msg, post) -> Comment:
    reply = int(msg.find(class_='tgme_widget_message_reply').get('href').split('/')[-1]) if msg.find(class_='tgme_widget_message_reply') else None
    return Comment(
        post, 
        int(msg.get('data-post-id')), 
        bs4.BeautifulSoup(str(msg.find(class_='js-message_text')).replace('<br/>', '\n'), 'html.parser').text, 
        reply, 
        BStoAuthor(msg), 
        msg.find(class_='tgme_widget_message_date').find('time').get('datetime')
    )

def BStoAuthor(msg) -> Author:
    author_username = msg.find(class_='tgme_widget_message_user').find('a').get('href').split('/')[-1] if msg.find(class_='tgme_widget_message_user') else None
    author_photo = msg.find(class_='tgme_widget_message_user_photo').find('img').get('src') if msg.find(class_='tgme_widget_message_user_photo') else None
    return Author(msg.find(class_='tgme_widget_message_author_name').text, author_username, author_photo)
