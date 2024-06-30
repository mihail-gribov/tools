from bs4 import BeautifulSoup
import markdownify

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

def get_data_channel(bs: BeautifulSoup) -> dict:
    info = bs.find(class_='tgme_channel_info')
    description = info.find(class_='tgme_channel_info_description').text if info.find(class_='tgme_channel_info_description') else None
    subscribers = parse_subscribers(info.find(class_='tgme_channel_info_counter').find(class_='counter_value').text)
    picture = info.find(class_='tgme_page_photo_image').find('img')['src'] if info.find(class_='tgme_page_photo_image') else None
    return {
        'name': info.find(class_='tgme_channel_info_header_title').text,
        'description': description,
        'subscribers': subscribers,
        'picture': picture,
        'data': bs
    }

def get_data_posts(bs: BeautifulSoup) -> list[dict]:
    result = []
    for post_bs in bs.find_all(class_='tgme_widget_message'):
        html_content = str(post_bs.find(class_='tgme_widget_message_text')).replace('<br/>', '\n') if post_bs.find(class_='tgme_widget_message_text') else None
        post_id = int(post_bs['data-post'].split('/')[-1])
        views = parse_subscribers(post_bs.find(class_='tgme_widget_message_views').text) if post_bs.find(class_='tgme_widget_message_views') else 0
        media = [
            {
                'url': photo.get('style').split("background-image:url('")[1].split("')")[0],
                'type': 'photo/jpg'
            } for photo in post_bs.find_all(class_='tgme_widget_message_photo_wrap')
        ] + [
            {
                'url': video['src'],
                'type': 'video/mp4'
            } for video in post_bs.find_all(class_='tgme_widget_message_video')
        ] + [
            {
                'url': round_video['src'],
                'type': 'round_video/mp4'
            } for round_video in post_bs.find_all(class_='tgme_widget_message_roundvideo')
        ] + [
            {
                'url': voice_msg['src'],
                'type': 'voice/ogg'
            } for voice_msg in post_bs.find_all(class_='tgme_widget_message_voice')
        ]
        datetime = post_bs.find(class_='datetime')['datetime'] if post_bs.find(class_='datetime') else post_bs.find(class_='time')['datetime']
        post_data = {
            'id': post_id,
            'html_content': html_content,
            'media': media,
            'views': views,
            'datetime': datetime
        }
        result.append(post_data)
    return result

    



def get_data_author(msg: BeautifulSoup) -> dict:
    author_username = msg.find(class_='tgme_widget_message_user').find('a').get('href').split('/')[-1] if msg.find(class_='tgme_widget_message_user') else None
    author_photo = msg.find(class_='tgme_widget_message_user_photo').find('img').get('src') if msg.find(class_='tgme_widget_message_user_photo') else None
    return {
        'name': msg.find(class_='tgme_widget_message_author_name').text,
        'username': author_username,
        'photo': author_photo
    }


# def get_data_post(bs: BeautifulSoup, channel_url: str) -> dict:
#     html_content = str(bs.find(class_='tgme_widget_message_text')).replace('<br/>', '\n') if bs.find(class_='tgme_widget_message_text') else None
#     post_id = int(bs.get('data-post').split('/')[-1])
#     views = parse_subscribers(bs.find(class_='tgme_widget_message_views').text) if bs.find(class_='tgme_widget_message_views') else 0
#     media = [
#         {
#             'url': photo.get('style').split("background-image:url('")[1].split("')")[0],
#             'type': 'photo/jpg'
#         } for photo in bs.find_all(class_='tgme_widget_message_photo_wrap')
#     ] + [
#         {
#             'url': video.get('src'),
#             'type': 'video/mp4'
#         } for video in bs.find_all(class_='tgme_widget_message_video')
#     ] + [
#         {
#             'url': round_video.get('src'),
#             'type': 'round_video/mp4'
#         } for round_video in bs.find_all(class_='tgme_widget_message_roundvideo')
#     ] + [
#         {
#             'url': voice_msg.get('src'),
#             'type': 'voice/ogg'
#         } for voice_msg in bs.find_all(class_='tgme_widget_message_voice')
#     ]
#     datetime = bs.find(class_='datetime').get('datetime') if bs.find(class_='datetime') else bs.find(class_='time').get('datetime')
#     return {
#         'channel_url': channel_url,
#         'url': f'{channel_url}/{post_id}',
#         'id': post_id,
#         'html_content': html_content,
#         'media': media,
#         'views': views,
#         'datetime': datetime,
#         'data': bs
#     }

def get_data_comment(msg: BeautifulSoup, post_url: str) -> dict:
    reply = int(msg.find(class_='tgme_widget_message_reply').get('data-reply-to')) if msg.find(class_='tgme_widget_message_reply') else None
    return {
        'post_url': post_url,
        'id': int(msg.get('data-post-id')),
        'html_content': str(msg.find(class_='js-message_text')).replace('<br/>', '\n'),
        'reply': reply,
        'author': get_data_author(msg),
        'datetime': msg.find(class_='tgme_widget_message_date').find('time').get('datetime')
    }