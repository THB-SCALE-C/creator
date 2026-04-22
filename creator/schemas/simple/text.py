from typing import ClassVar
from pydantic import BaseModel

class Text(BaseModel):
    slide_type:ClassVar = "text"
    title: str
    text: str