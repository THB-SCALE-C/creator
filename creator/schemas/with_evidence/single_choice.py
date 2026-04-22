from typing import ClassVar
from pydantic import BaseModel, Field


class Item(BaseModel):
    question: str
    correct_answer: str 
    wrong_answers: list[str]


class SingleChoice(BaseModel):
    slide_type:ClassVar = "single_choice"
    title: str
    question_items: list[Item]
    tip: str
    positive_feedback: str
    negative_feedback: str
    evidences:list = Field(description="A list of document IDs that support your statements for this slide. Leave empty if no relevant statements are made.", default_factory=list)
