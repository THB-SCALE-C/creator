from typing import Union
from .text import TextWithEvidence
from .drag_text import DragTextWithEvidence
from .single_choice import SingleChoiceWithEvidence

SlideTypeUnion = Union[TextWithEvidence,DragTextWithEvidence,SingleChoiceWithEvidence]

__all__ = [
    "TextWithEvidence",
    "DragTextWithEvidence",
    "SingleChoiceWithEvidence",
    "SlideTypeUnion"
]