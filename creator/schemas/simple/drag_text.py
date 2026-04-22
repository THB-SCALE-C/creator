from typing import ClassVar
from pydantic import BaseModel, Field


class DragText(BaseModel):
    slide_type:ClassVar = "drag_text"
    title: str = Field()
    user_instruction: str = Field(
        description="Instructions for the student on how to solve the cloze text. DO NOT MENTION the surrounding `*`.")
    cloze_text: str = Field(
        description="The cloze test content. Surround missing words with '*' (e.g., *Addition*).")
    distractors:list[str] = Field(description="A list of similar words that distract the user.")


