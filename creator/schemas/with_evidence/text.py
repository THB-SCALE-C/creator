from typing import ClassVar
from pydantic import BaseModel, Field

class Text(BaseModel):
    slide_type:ClassVar = "text"
    title: str
    text: str
    evidences:list = Field(description="A list of document IDs that support your statements for this slide. Leave empty if no relevant statements are made.", default_factory=list)
