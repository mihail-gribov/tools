from .base_model import BaseModel

class Author(BaseModel):
    """Represents an author with basic attributes and methods."""
    
    url_template: str = "https://t.me/{username}"

    def __init__(self, client, id):
        """Initializes an Author instance with client and id."""
        super().__init__(client, id)
        self.name = ''
        self.username = ''
        self.photo = ''
    
    def get_html(self) -> str:
        """Returns a basic HTML representation of the author."""
        return f"<div><h1>{self.name}</h1><p>@{self.username}</p></div>"
