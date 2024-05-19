from . import parsers
from . import telegram_async


class BaseModel:
    url_template: str = ""

    def __init__(self, data: dict = None) -> None:
        if data:
            for key, value in data.items():
                setattr(self, key, value)

    async def to_dict(self) -> dict:
        data = {}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, BaseModel):
                data[key] = await value.to_dict()
            elif isinstance(value, list):
                data[key] = [await item.to_dict() if isinstance(item, BaseModel) else item for item in value]
            else:
                data[key] = value
        return data

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def get_html(self) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

    def get_text(self) -> str:
        return parsers.html_to_text(self.get_html())

    def get_markdown(self) -> str:
        return parsers.html_to_markdown(self.get_html())

    def get_url(self) -> str:
        return self.url_template.format(**self.__dict__)


class Media(BaseModel):
    url_template: str = ""

    def __init__(self, data: dict = None) -> None:
        self.url = ''
        self.type = ''
        super().__init__(data or {})


class Author(BaseModel):
    url_template: str = "https://t.me/{username}"

    def __init__(self, data: dict = None) -> None:
        self.name = ''
        self.username = ''
        self.photo = ''
        super().__init__(data or {})


class Comment(BaseModel):
    url_template: str = "https://t.me/{post.channel.url}/{post.id}?comment={id}"

    def __init__(self, data: dict = None) -> None:
        self.post = None
        self.id = 0
        self.html_content = ''
        self.reply = None
        self.author = None
        self.datetime = ''
        super().__init__(data or {})

    def get_html(self) -> str:
        return self.html_content


class Post(BaseModel):
    url_template: str = "https://t.me/{channel.url}/{id}"

    def __init__(self, data: dict = None) -> None:
        self.channel = None
        self.url = ''
        self.id = 0
        self.html_content = ''
        self.media = []
        self.views = 0
        self.datetime = ''
        self.__data = None
        super().__init__(data or {})

    async def get_comments(self, limit=10) -> list[Comment] | None:
        return await telegram_async.get_comments(self, limit)

    async def get_comment(self, comment_id: int) -> Comment | None:
        return await telegram_async.get_comment(self, comment_id)

    def get_html(self) -> str:
        return self.html_content


class Channel(BaseModel):
    url_template: str = "https://t.me/{url}"

    def __init__(self, data: dict = None) -> None:
        self.private = False
        self.url = ''
        self.name = ''
        self.description = ''
        self.subscribers = 0
        self.picture = ''
        self.__data = None
        self.__posts = {}
        super().__init__(data or {})

    async def get_post(self, post_id: int) -> Post | None:
        return await telegram_async.get_post(self, post_id)

    async def get_latest(self) -> list[Post]:
        return [parsers.bs_to_post(post, self) for post in self.__data.find_all(class_='tgme_widget_message')]

    async def get_all_posts(self) -> list[Post]:
        if not self.__posts:
            self.__posts = await telegram_async.get_all_posts(self)
        return self.__posts

    async def is_public(self) -> bool:
        return not self.private

    async def is_private(self) -> bool:
        return self.private
