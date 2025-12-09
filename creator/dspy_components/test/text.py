from dspy import Signature, OutputField
from pydantic import BaseModel

class Text(BaseModel):
    title: str
    text: str