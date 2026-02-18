from typing import ClassVar
from dspy import Signature, OutputField
from pydantic import BaseModel

class Text(BaseModel):
    slide_type:ClassVar = "text"
    title: str
    text: str