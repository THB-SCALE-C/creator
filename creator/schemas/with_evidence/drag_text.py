from typing import ClassVar
from pydantic import BaseModel, Field
from creator.schemas.simple.drag_text import DragText



class DragTextWithEvidences(DragText):
    evidences:list = Field(description="A list of document IDs that support your statements for this slide. Leave empty if no relevant statements are made.", default_factory=list)

