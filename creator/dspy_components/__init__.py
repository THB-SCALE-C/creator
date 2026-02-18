from typing import ClassVar
from openai import BaseModel
from .base.text import Text
from .base.cloze import ClozeTest
from .base.single_choice import SingleChoice


__all__ = [
    "Text",
    "ClozeTest",
    "SingleChoice",
]