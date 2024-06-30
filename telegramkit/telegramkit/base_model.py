from .parsers import html_to_text, html_to_markdown

class BaseModel:
    """Base class for models with common attributes and methods."""
    
    url_template: str = ""

    def __init__(self, client, id) -> None:
        """Initializes a BaseModel instance with client and id."""
        self.client = client
        self.id = id
        
    def from_dict(self, data: dict):
        """Populates the model's attributes from a dictionary."""
        if data:
            for key, value in data.items():
                setattr(self, key, value)

    async def to_dict(self) -> dict:
        """Converts the model's attributes to a dictionary."""
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
        """Returns a string representation of the model."""
        return f"{self.__class__.__name__}({self.__dict__})"

    def get_html(self) -> str:
        """Returns an HTML representation of the model. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")

    def get_text(self) -> str:
        """Converts the HTML representation to plain text."""
        return html_to_text(self.get_html())

    def get_markdown(self) -> str:
        """Converts the HTML representation to Markdown format."""
        return html_to_markdown(self.get_html())

    def get_url(self) -> str:
        """Generates a URL for the model based on the url_template."""
        return self.url_template.format(**self.__dict__)
