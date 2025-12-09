from typing import Any
import uuid


def single_choice(element_conf: dict[str, Any]):
    choices = []
    for choice in element_conf["questions"]:
        correct_answer = choice["correct_answer"]
        wrong_answers = choice["wrong_answers"]
        answers = [correct_answer, *wrong_answers]
        _choice = {
            **choice,
            "subContentId": str(uuid.uuid1()),
            "answers": answers
        }
        del _choice["correct_answer"]
        del _choice["wrong_answers"]
        choices.append(_choice)
    return {**element_conf, "choices": choices}
