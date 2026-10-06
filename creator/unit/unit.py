from copy import deepcopy
from typing import Any, Iterable, List, Literal
from dspy import Prediction
from pydantic import BaseModel
from creator.schemas.base import BaseComponent
from creator.unit_assembler.UnitAssembler import UnitAssembler
from creator.schemas.simple import Text, DragText, SingleChoice
from creator.schemas.with_evidence.text import TextWithEvidence
from creator.schemas.with_evidence.drag_text import DragTextWithEvidence
from creator.schemas.with_evidence.single_choice import SingleChoiceWithEvidence
from ..lib.vis import render_learning_content

_MODEL_DUMP_SUPPORTS_EXCLUDE_COMPUTED = (
    "exclude_computed_fields" in BaseModel.model_dump.__code__.co_varnames
)


class Unit(Prediction):
    assembler = UnitAssembler()

    @classmethod
    def from_dict(cls, data: dict) -> "Unit":
        title = data["title"]
        slide_data = data["slides"]
        slide_types = {
            "text": Text,
            "drag_text": DragText,
            "single_choice": SingleChoice,
        }
        slide_types_with_evidence = {
            "text": TextWithEvidence,
            "drag_text": DragTextWithEvidence,
            "single_choice": SingleChoiceWithEvidence,
        }
        slides = []
        for raw_slide in slide_data:
            slide_type = raw_slide.get("type")
            if "evidences" in raw_slide:
                slide_cls = slide_types_with_evidence.get(slide_type)
            else:
                slide_cls = slide_types.get(slide_type)
            if slide_cls is None:
                raise ValueError(f"Unsupported slide type: {slide_type!r}")
            slides.append(slide_cls.model_validate(raw_slide))
        return cls(slides=slides, title=title)

    def __init__(self, slides: List[BaseComponent], title: str, *args, **kwargs) -> None:
        super().__init__(slides=slides, title=title, *args, **kwargs)

    def to_html(self):
        return render_learning_content(self.to())

    def to(self, exclude_computed_fields: bool = False, ignore_keys: list[str] = ["reasoning"], mode: Literal["dict", "unit"] = "dict", as_slides: bool = True, annotate: bool = True):
        if mode not in ("dict", "unit"):
            raise ValueError("mode must be either 'dict' or 'unit'.")

        forbidden = set(ignore_keys)
        data = _content_items(self, forbidden)

        if as_slides:
            slides = getattr(self, "slides", None)
            if slides is None:
                slides = []
                for key, value in data.items():
                    if key != "title":
                        if annotate:
                            value._key = key
                        slides.append(value)
            if not slides:
                raise ValueError(
                    "No attribute `slides` found. Incomplete learning unit.")
            if annotate:
                for i, slide in enumerate(slides):
                    slide._index = i

            if mode == "dict":
                _slides = []
                for slide in slides:
                    _slide = _to_dict(slide, exclude_computed_fields=exclude_computed_fields)
                    if isinstance(_slide, dict) and annotate:
                        _slide["index"] = slide._index
                        if key:=getattr(slide,"_key",None):
                            _slide["key"] = slide._key
                    _slides.append(_slide)
                slides = _slides
                return {"title": self.title, "slides": slides}

            unit_data: dict[str, Any] = {
                "title": self.title, "slides": list(slides)}
            return Unit(**unit_data)

        if mode == "dict":
            return _to_dict(data, exclude_computed_fields=exclude_computed_fields)

        unit_data = deepcopy(data) if exclude_computed_fields else data.copy()
        return Unit(**unit_data)

    def to_h5p(self, output_dir=".out", out_name="unit.h5p", template_path: str | None = None):
        content = self.to()
        if template_path:
            self.assembler.set_template_path(template_path=template_path)
        assembled_content = self.assembler.assemble_content(
            content)  # type: ignore
        assembled_unit_path = self.assembler.assemble_h5p(
            assembled_content, output_dir, out_name)
        return assembled_unit_path


def _content_items(unit: Unit, ignore_keys: set[str]) -> dict[str, Any]:
    return {key: value for key, value in unit.items() if key not in ignore_keys}


def _to_dict(data, exclude_computed_fields: bool = True):
    if not data:
        return data
    if hasattr(data, "model_dump"):
        try:
            return data.model_dump(exclude_computed_fields=exclude_computed_fields)
        except:
            return data.model_dump()
    if isinstance(data, dict):
        return {key: _to_dict(value,exclude_computed_fields) for key, value in data.items()}
    if isinstance(data, (list, tuple)):
        return [_to_dict(el, exclude_computed_fields) for el in data]
    return data