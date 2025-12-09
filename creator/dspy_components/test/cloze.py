from pydantic import BaseModel, Field

class ClozeTest(BaseModel):
    title: str = Field()
    user_instruction: str = Field(
        description="Instructions for the student on how to solve the cloze text.")
    cloze_text: str = Field(
        description="The cloze test content. Surround missing words with '*' (e.g., *Addition*).")


