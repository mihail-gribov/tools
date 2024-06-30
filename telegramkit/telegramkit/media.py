from .base_model import BaseModel

class Media(BaseModel):
    url_template: str = ""

    def __init__(self, client, id):
        super().__init__(client, id)
        self.url = ''
        self.type = ''

    def get_html(self) -> str:
        if self.type.startswith('photo'):
            return f'<img src="{self.url}" alt="photo">'
        elif self.type.startswith('video') or self.type == 'round_video/mp4':
            return f'<video controls><source src="{self.url}" type="{self.type}"></video>'
        elif self.type == 'voice/ogg':
            return f'<audio controls><source src="{self.url}" type="{self.type}"></audio>'
        elif self.type.startswith('audio'):
            return f'<audio controls><source src="{self.url}" type="{self.type}"></audio>'
        elif self.type.startswith('document'):
            return f'<a href="{self.url}">Download document</a>'
        elif self.type.startswith('animation'):
            return f'<video controls loop autoplay><source src="{self.url}" type="{self.type}"></video>'
        else:
            return f'<a href="{self.url}">View file</a>'
