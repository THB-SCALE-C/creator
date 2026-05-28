from typing import Union
from .text import TextWithEvidence
from .drag_text import DragTextWithEvidences
from .single_choice import SingleChoiceWithEvidence

SlideTypeUnion = Union[TextWithEvidence,DragTextWithEvidences,SingleChoiceWithEvidence]

__all__ = [
    "TextWithEvidence",
    "DragTextWithEvidences",
    "SingleChoiceWithEvidence",
    "SlideTypeUnion"
]