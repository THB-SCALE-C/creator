from dspy import Signature, OutputField

class Text(Signature):
    title: str = OutputField()
    text: str = OutputField()