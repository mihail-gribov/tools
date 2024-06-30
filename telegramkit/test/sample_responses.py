# channel_html с полным набором данных
channel_html = """
<html>
    <div class='tgme_channel_info'>
        <div class='tgme_channel_info_header_title'>Test Channel</div>
        <div class='tgme_channel_info_description'>Description</div>
        <div class='tgme_channel_info_counter'>
            <span class='counter_value'>1.5K</span>
        </div>
        <div class='tgme_page_photo_image'>
            <img src='https://example.com/picture.jpg' />
        </div>
    </div>
</html>
"""

# channel_html без описания
channel_html_no_description = """
<html>
    <div class='tgme_channel_info'>
        <div class='tgme_channel_info_header_title'>Test Channel</div>
        <div class='tgme_channel_info_counter'>
            <span class='counter_value'>1.5K</span>
        </div>
        <div class='tgme_page_photo_image'>
            <img src='https://example.com/picture.jpg' />
        </div>
    </div>
</html>
"""

# post_html с полным набором данных
post_html = """
<html>
    <div class='tgme_widget_message' data-post='/testchannel/1'>
        <div class='tgme_widget_message_text'>Test post content</div>
        <div class='tgme_widget_message_views'>123</div>
        <div class='datetime' datetime='2022-01-01T12:00:00'></div>
    </div>
</html>
"""

# post_html без просмотров
post_html_no_views = """
<html>
    <div class='tgme_widget_message' data-post='/testchannel/1'>
        <div class='tgme_widget_message_text'>Test post content</div>
        <div class='datetime' datetime='2022-01-01T12:00:00'></div>
    </div>
</html>
"""

# post_html без текста сообщения
post_html_no_text = """
<html>
    <div class='tgme_widget_message' data-post='/testchannel/1'>
        <div class='tgme_widget_message_views'>123</div>
        <div class='datetime' datetime='2022-01-01T12:00:00'></div>
    </div>
</html>
"""
