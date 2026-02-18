
from typing import ClassVar
from pydantic import BaseModel


class BaseComponent(BaseModel):
    slide_type:ClassVar[str]