from typing import Any
import uuid


def single_choice(element_conf: dict[str, Any]):
    choices = []
    for choice in element_conf["choices"]:
        answers = choice["answers"]
        answers.sort(key=lambda a: not (
            a["correct"] is True or
            (isinstance(a["correct"], str)
                and a["correct"].lower() == "true")
        ))
        _choice = {
            **choice,
            "subContentId": str(uuid.uuid1()),
            "answers": [a["text"] for a in answers]
        }
        choices.append(_choice)
    return {**element_conf, "choices": choices}
