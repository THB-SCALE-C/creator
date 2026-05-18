from typing import ClassVar
from creator.schemas.base import BaseComponent

class Text(BaseComponent):
    slide_type:ClassVar = "text"
    title: str
    text: str