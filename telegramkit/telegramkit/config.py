import random

version = '1.0.0'
use_random_user_agent = True
request_header = {
    'User-Agent': '1'
}

if use_random_user_agent:
    operating_systems = ['Windows', 'MacOS', 'Linux', 'iPhone', 'Android', 'iPad', 'Chrome OS']
    browsers = [
        'Chrome 100', 'Chrome 101', 'Chrome 102',
        'Firefox 93', 'Firefox 94', 'Firefox 95',
        'Safari 14', 'Safari 15',
        'Opera 30', 'Opera 31',
        'Edge 90', 'Edge 91', 'Edge 92'
    ]
    request_header['User-Agent'] = f"{random.choice(operating_systems)}; {random.choice(browsers)}"
