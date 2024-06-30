from .base_model import BaseModel

class Author(BaseModel):
    url_template: str = "https://t.me/{username}"

    def __init__(self, client, id):
        super().__init__(client, id)
        self.name = ''
        self.username = ''
        self.photo = ''
    
    def get_html(self) -> str:
        return f"<div><h1>{self.name}</h1><p>@{self.username}</p></div>"

