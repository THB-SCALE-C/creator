
from typing import ClassVar, Literal
from pydantic import BaseModel, Field

PhaseType = Literal["introduction","acquisition","assessment","conclusion"]

class BaseComponent(BaseModel):
    type:ClassVar[str]
    phase: PhaseType = Field(
        description="The phase of the unit this slide belongs to.")
    

