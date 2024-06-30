from .parsers import html_to_text, html_to_markdown

class BaseModel:
    url_template: str = ""

    def __init__(self, client, id) -> None:
        self.client = client
        self.id = id
        
    def from_dict(self, data: dict):
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
        return html_to_text(self.get_html())

    def get_markdown(self) -> str:
        return html_to_markdown(self.get_html())

    def get_url(self) -> str:
        return self.url_template.format(**self.__dict__)
