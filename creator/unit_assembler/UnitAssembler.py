"""
General assembler logic that can be configured via config.yml
"""
import json
from pathlib import Path
from typing import Any
from jinja2 import Environment, FileSystemLoader, Template
import uuid

from ..lib.loader import load_yaml
from ..lib.types import AssemblerConfig
from ..lib.zip_folder import zip_folder
from . import preprocess

FOLDER_PATH = Path(__file__).resolve().parent

class UnitAssembler:
    _config: AssemblerConfig
    _unit_template_path: str | None = None
    _jinja_templates_path: str | None = None
    _templates: dict[str, Template] | None = None

    def __init__(self, config: AssemblerConfig | dict[str, Any] = {}) -> None:
        type(self)._ensure_initialized(config)

    @classmethod
    def _ensure_initialized(cls, config: AssemblerConfig | dict[str, Any] | None = None) -> None:
        if cls._config is not None and config is None:
            return

        cls._config = load_yaml(FOLDER_PATH / "config.yml")
        if config:
            cls._config.update(config)  # type: ignore

        cls._unit_template_path = cls._config["settings"]["unit_template_path"]  # type: ignore[index]
        cls._jinja_templates_path = cls._config["settings"]["jinja_templates_path"]  # type: ignore[index]
        cls._templates = _load_jinja_templates_from_dir(
            FOLDER_PATH / f"resources/templates/jinja/{cls._jinja_templates_path}"
        )

    @classmethod
    def assemble_content(cls, intermediate_content: dict[str, Any]) -> str:
        cls._ensure_initialized()
        if cls._templates is None or cls._config is None:
            raise RuntimeError("UnitAssembler is not initialized.")

        final_slides = []
        main_template = cls._templates["main"]

        # get unit tile for cover page
        unit_title = intermediate_content.get(
            "title", cls._config["defaults"]["unit_title"])

        # render slide content as elements
        for slide_conf in intermediate_content.get("slides", []):
            slide_title = slide_conf.get("title", "")
            slide_type = slide_conf["type"]
            slide_template_config = cls._config["slide_types"][slide_type]
            element_template = cls._templates[slide_template_config["template_key"]]

            element_conf = {"uuid": str(uuid.uuid1())}
            preprocess_fn_name = slide_template_config.get("preprocess", None)
            if preprocess_fn_name:
                preprocess_fn = getattr(
                    preprocess, preprocess_fn_name)
                _slide = preprocess_fn(slide_conf)
                element_conf.update(_slide)
            else:
                element_conf.update(slide_conf)
            element = json.loads(element_template.render(element_conf))
            final_slides.append({"element": element, "title": slide_title, "type": slide_conf.get(
                "type", ""), "element_config": element_conf})

        # manufacture the final presentation
        presentation = main_template.render(
            {"slides": final_slides, "title": unit_title})
        return presentation

    @classmethod
    def assemble_h5p(cls, presentation: str,output_dir:str|Path=".out", out_name: str = "unit.h5p"):
        cls._ensure_initialized()
        if cls._unit_template_path is None:
            raise RuntimeError("UnitAssembler is not initialized.")

        contents = [{
            "filename": "content.json",
            "path": "content",
            "content": presentation
        }]
        zip_path = FOLDER_PATH / f"resources/templates/units/{cls._unit_template_path}"
        buffer = zip_folder(str(zip_path), contents=contents)  # type: ignore
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / out_name
        output_path.write_bytes(buffer)
        return output_path


def _load_jinja_templates_from_dir(
    root_folder: str | Path = "",
) -> dict[str, Template]:
    templates = {}
    env = Environment(loader=FileSystemLoader(root_folder))
    for tmplt in env.list_templates():
        templates[tmplt.split(".")[0]] = env.get_template(tmplt)
    return templates
