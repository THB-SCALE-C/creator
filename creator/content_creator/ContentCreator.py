
from typing import Any, Type, Union
from warnings import warn
import dspy
from dspy import Signature, Prediction, ChainOfThought, Module

from creator.unit_assembler.UnitAssembler import UnitAssembler
from ..dspy_components.base.cloze import ClozeTest
from ..dspy_components.base.single_choice import SingleChoice
from ..dspy_components.base.text import Text
from ..lib.types import SignatureSlide
from ..lib.vis import render_learning_content
from ..llm import OPENROUTER_DSPY_LM_CONFIG

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


class CreatorOutput:
    def __init__(self, pred: Prediction | ChainOfThought) -> None:
        self.pred = pred

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
        UnitAssembler.set_config(template_path)
        content = self.to_dict()
        assembled_content = UnitAssembler.assemble_content(content)
        assembled_unit_path = UnitAssembler.assemble_h5p(
            assembled_content, output_dir, out_name)
        return assembled_unit_path


class ContentCreator:
    def __init__(self, model_id: str = "openrouter/openai/gpt-oss-120b", **model_props) -> None:
        self._lu_sig = None
        self._output = None
        self.predictor = None
        self.LM = dspy.LM(
            **OPENROUTER_DSPY_LM_CONFIG,
            **model_props,
            model=model_id,
        )
        self._default_unit = LEARNING_UNIT

    def invoke(self, topic: str, **kwargs):
        if not self.predictor:
            self._set_predictor()
        if not self.predictor:
            raise ValueError("No predictor found.")
        _out = self.predictor(topic=topic, **kwargs)
        if not _out:
            raise ValueError("No output.")
        self._output = CreatorOutput(_out)
        return self._output

    def enable_cot(self):
        """Adds chain of thought."""
        if not self._lu_sig:
            raise ValueError("No signature found. Cannot create predictor.")
        self.predictor = dspy.ChainOfThought(self._lu_sig)
        self.predictor.set_lm(self.LM)

    def _set_predictor(self):
        if not self._lu_sig:
            raise ValueError("No signature found. Cannot create predictor.")
        self.predictor = dspy.Predict(self._lu_sig)
        self.predictor.set_lm(self.LM)

    def add_instructions(self, instructions: str):
        """adds instructions; must be set after learning unit signature"""
        if not self._lu_sig:
            raise ValueError("No signature found. Cannot add instructions")
        self._lu_sig = self._lu_sig.with_instructions(instructions)

    def set_lu_signature(self, lu_sig: Type[Signature]):
        """
        Signature must cohere to the format:
         class Unit(Signature):
            title: str
            slides: list[type[Signature]] | type[Signature]

        :param self: Description
        :param lu_sig: Description
        :type lu_sig: Type[Signature]
        """
        if self._lu_sig:
            warn("learning unit's signature already set! Overwritting...")
        self._lu_sig = lu_sig

    def set_lu_signature_with_json(self, slides: list[SignatureSlide], free_choice=False, **kwargs):
        if self._lu_sig:
            warn("learning unit signature already set! Overwritting...")
        if free_choice:
            _types = tuple([MAP_R[slide["type"]] for slide in slides])
            _slide_type = Union[_types]
            self._lu_sig = self._default_unit.insert(-1, "slides",
                                                     dspy.OutputField(
                                                         desc=f"For the possible slides types, take in regard these instructions:\n\n {"\n\n".join([f'##{slide["name"]}\n{slide["desc"]}' for slide in slides])}"),
                                                     list[_slide_type])
        else:
            self._lu_sig = self._default_unit.insert(-1, "slides",
                                                     dspy.OutputField(), _to_signature(slides))
        if kwargs:
            for key, val in kwargs.items():
                if key.startswith("input_"):
                    key = key.removeprefix("input_")
                    self._lu_sig = self._lu_sig.insert(
                        -1, key, dspy.InputField(desc=val), str)
                else:
                    key = key.removeprefix("output_")
                    self._lu_sig = self._lu_sig.insert(
                        -1, key, dspy.OutputField(desc=val), str)

    def set_dspy_module_predictor(self, module: type[Module]):
        """
        Lets you create a module as predictor. The output signature must cohere to the expected format:
         class Unit(Signature):
            title: str
            slides: list[type[Signature]] | type[Signature]

        :param self: Description
        :param module: Description
        :type module: type[Module]
        """
        self.predictor = module()
        self.predictor.set_lm(self.LM)


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


def _to_signature(data: list[Any] | dict[str, Any], name: str = "Slides") -> Type[Signature]:
    class Wrapper(Signature):
        pass
    sig = Wrapper
    if isinstance(data, list):
        for i, d in enumerate(data):
            if isinstance(d, dict):
                type_ = MAP_R[d["type"]]
                name = d["name"]
                multiple = d.get("multiple", False)
                sig = sig.insert(i, name, dspy.OutputField(
                    desc=d["desc"]), type_=list[type_] if multiple else type_)
            else:
                raise ValueError(
                    f"Expected dict, received {d.__class__.__name__}")
    sig.__name__ = name
    return sig


def _parse_to_dict(slide):
    if isinstance(slide, list):
        return [_parse_to_dict(v) for v in slide]
    if isinstance(slide, dict):
        return {k: _parse_to_dict(v) for k, v in slide.items()}
    if hasattr(slide, "__dict__"):
        return {k: _parse_to_dict(v) for k, v in dict(slide).items()}
    return slide
