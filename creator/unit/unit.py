from typing import Any
import dspy
from dspy import Signature, Prediction
from creator.dspy_components.__base__ import BaseComponent
from creator.unit_assembler.UnitAssembler import UnitAssembler
from ..lib.vis import render_learning_content


class LEARNING_UNIT(dspy.Signature):
    topic: str = dspy.InputField()
    title: str = dspy.OutputField()


class REWORK_LEARNING_UNIT(dspy.Signature):
    last_output: type[Signature] | dict[str, Any] = dspy.InputField()
    user_feedback_history = dspy.InputField()
    title: str = dspy.OutputField()


class Unit:
    def __init__(self, pred: Prediction) -> None:
        self.pred: Prediction = pred
        self.assembler = UnitAssembler()
        if hasattr(pred, "slides"):
            self.slides = pred.slides
        else:
            raise ValueError("Incomplete unit, no `slides`.")
        if hasattr(pred, "title"):
            self.title = pred.title
        else:
            raise ValueError("Incomplete unit, no `title`.")
        self.reasoning = pred.reasoning if hasattr(pred, "reasoning") else None

    def __repr__(self) -> str:
        return self.pred.__repr__()

    def to_html(self):
        return render_learning_content(self.to_dict())

    def to_dict(self):
        if not self.pred:
            raise ValueError("No prediction object found. Invoke first.")
        slides = self.pred.get("slides", None)
        if not slides:
            raise ValueError(
                "No attribute `slides` found. Incomplete learning unit.")
        _slides = _to_json(list(slides))  # type: ignore
        return {**self.pred.toDict(), "slides": _slides}  # type:ignore

    def to_h5p(self, output_dir=".out", out_name="unit.h5p", template_path: str | None = None):
        if not self.pred:
            raise ValueError("No learning unit created. Create first.")
        content = self.to_dict()
        if template_path:
            self.assembler.set_template_path(template_path=template_path)
        assembled_content = self.assembler.assemble_content(content)
        assembled_unit_path = self.assembler.assemble_h5p(
            assembled_content, output_dir, out_name)
        return assembled_unit_path


def _to_json(slides: list[BaseComponent]):
    _slides = []
    for slide in slides:
        _slide = slide.model_dump()
        _slide.setdefault("type", slide.slide_type)
        _slides.append(_slide)
    return _slides
