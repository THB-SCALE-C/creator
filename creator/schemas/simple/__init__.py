from typing import Union
from .text import Text
from .drag_text import DragText
from .single_choice import SingleChoice

SlideTypeUnion = Union[Text,DragText,SingleChoice]

__all__ = [
    "Text",
    "DragText",
    "SingleChoice",
    "SlideTypeUnion"
]