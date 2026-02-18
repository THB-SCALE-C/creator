from typing import ClassVar
from pydantic import BaseModel


class Question(BaseModel):
    question: str
    correct_answer: str 
    wrong_answers: list[str]


class SingleChoice(BaseModel):
    slide_type:ClassVar = "single_choice"
    title: str
    questions: list[Question]
    tip: str
    positive_feedback: str
    negative_feedback: str