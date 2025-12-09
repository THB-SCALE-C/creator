from typing import Literal, TypedDict, Dict, Optional



class Settings(TypedDict):
    jinja_templates_path: str
    unit_template_path: str


class Defaults(TypedDict):
    unit_title: str


class SlideType(TypedDict):
    template_key: str
    preprocess: Optional[str]


class AssemblerConfig(TypedDict):
    settings: Settings
    defaults: Defaults
    slide_types: Dict[str, SlideType]


class SignatureSlide(TypedDict):
    type:Literal["text","single_choice","drag_text"]
    desc:str
    name:str
    multiple:bool|None 