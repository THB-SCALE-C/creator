from typing import ClassVar
from pydantic import BaseModel


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