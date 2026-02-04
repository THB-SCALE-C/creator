
from typing import Any, Type, Union
from warnings import warn
import dspy
from dspy import Signature, Prediction, ChainOfThought, Module
from llm.provider.openrouter import OpenrouterLM

from creator.unit_assembler.UnitAssembler import UnitAssembler
from ..dspy_components.base.cloze import ClozeTest
from ..dspy_components.base.single_choice import SingleChoice
from ..dspy_components.base.text import Text
from ..lib.types import SignatureSlide
from ..lib.vis import render_learning_content

MAP = {
    "Text": "text",
    "SingleChoice": "single_choice",
    "ClozeTest": "drag_text",
}
MAP_R = {
    "text": Text,
    "single_choice": SingleChoice,
    "drag_text": ClozeTest,
}


class LEARNING_UNIT(dspy.Signature):
    topic: str = dspy.InputField()
    title: str = dspy.OutputField()


class REWORK_LEARNING_UNIT(dspy.Signature):
    last_output: type[Signature] | dict[str, Any] = dspy.InputField()
    user_feedback_history = dspy.InputField()
    title: str = dspy.OutputField()


class Unit:
    def __init__(self, pred: Prediction | ChainOfThought) -> None:
        self.pred = pred
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
        if not self.pred.slides:
            raise ValueError(
                "No slides object found. Incomplete learning unit.")
        _slides = _to_json(self.pred.slides)
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


def _to_json(slides: list[Any] | Any, map=MAP):
    _slides = []
    for slide in slides if isinstance(slides, list) else dict(slides).values():
        if isinstance(slide, list):
            _slides.extend([{**dict(s), "type": map[s.__class__.__name__]}
                            for s in slide])
        else:
            _slide = {**dict(slide), "type": map[slide.__class__.__name__]}
            _slides.append(_slide)
        # recursivly parsing signature and signature members to nested dict
        _slides = [_parse_to_dict(s) for s in _slides]
    return _slides


def _parse_to_dict(slide):
    if isinstance(slide, list):
        return [_parse_to_dict(v) for v in slide]
    if isinstance(slide, dict):
        return {k: _parse_to_dict(v) for k, v in slide.items()}
    if hasattr(slide, "__dict__"):
        return {k: _parse_to_dict(v) for k, v in dict(slide).items()}
    return slide
