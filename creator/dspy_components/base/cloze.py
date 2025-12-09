from dspy import Signature, OutputField

class ClozeTest(Signature):
    title: str = OutputField()
    user_instruction: str = OutputField(
        desc="Instructions for the student on how to solve the cloze text.")
    cloze_text: str = OutputField(
        desc="The cloze test content. Surround missing words with '*' (e.g., *Addition*).")


