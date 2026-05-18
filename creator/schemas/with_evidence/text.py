from pydantic import Field
from creator.schemas.simple.text import Text

class TextWithEvidence(Text):
    evidences:list = Field(description="A list of document IDs that support your statements for this slide. Leave empty if no relevant statements are made.", default_factory=list)
