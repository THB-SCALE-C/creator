from dspy import Signature, OutputField


class _Question(Signature):
    question: str = OutputField()
    correct_answer: str = OutputField()
    wrong_answers: list[str] = OutputField()


class SingleChoice(Signature):
    title: str = OutputField()
    questions: list[_Question] = OutputField()
    tip: str = OutputField()
    positive_feedback: str = OutputField()
    negative_feedback: str = OutputField()