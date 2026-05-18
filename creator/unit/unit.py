from typing import List
from dspy import Prediction
from creator.schemas.base import BaseComponent
from creator.unit_assembler.UnitAssembler import UnitAssembler
from creator.schemas.simple import Text, DragText, SingleChoice
from creator.schemas.with_evidence.text import TextWithEvidence
from creator.schemas.with_evidence.drag_text import DragTextWithEvidences
from creator.schemas.with_evidence.single_choice import SingleChoiceWithEvidence
from ..lib.vis import render_learning_content

class Unit(Prediction):

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
            "drag_text": DragTextWithEvidences,
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

    def __init__(self, slides:List[BaseComponent], title:str,*args, **kwargs) -> None:
        super().__init__(slides=slides, title=title, *args, **kwargs)
        self.assembler = UnitAssembler()

    def to_html(self):
        return render_learning_content(self.to_dict())

    def to_dict(self):
        slides = getattr(self,"slides", None)
        if not slides:
            raise ValueError(
                "No attribute `slides` found. Incomplete learning unit.")
        _slides = _to_json(list(slides))  # type: ignore
        return {"title":self.title, "slides": _slides}  # type:ignore

    def to_h5p(self, output_dir=".out", out_name="unit.h5p", template_path: str | None = None):
        content = self.to_dict()
        if template_path:
            self.assembler.set_template_path(template_path=template_path)
        assembled_content = self.assembler.assemble_content(content)
        assembled_unit_path = self.assembler.assemble_h5p(
            assembled_content, output_dir, out_name)
        return assembled_unit_path


def _to_json(slides: list[BaseComponent]):
    _slides = []
    for i,slide in enumerate(slides):
        _slide = slide.model_dump()
        _slide.setdefault("type", slide.slide_type)
        _slide["index"] = i
        _slides.append(_slide)
    return _slides
