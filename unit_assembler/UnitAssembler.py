"""
General assembler logic that can be configured via config.yml
"""
from pathlib import Path
from typing import Any
from typing_extensions import Buffer
import uuid
import preprocess
from supabase import Client
from lib.loader import load_jinja_templates, load_yaml


class UnitAssembler:
    def __init__(self, supabase: Client, config_path: Path = Path("config.yml")) -> None:
        self.config = load_yaml(config_path)
        self.templates = load_jinja_templates(
            supabase=supabase,
            bucket=self.config["settings"]["bucket"],
            root_folder=self.config["settings"]["template_paths"]["element_templates_folder"],
        )
        self.unit_template_path = self.config["settings"]["template_paths"]["unit_template_path"]

    def assemble_content(self, intermediate_content: dict[str, Any]) -> str:
        final_slides = []
        main_template = self.templates["main"]

        # get unit tile for cover page
        unit_title = intermediate_content.get(
            "title", self.config["defaults"]["unit_title"])

        # render slide content as elements
        for slide_conf in intermediate_content.get("slides", []):
            slide_title = slide_conf.get("title", "Slide")
            slide_type = slide_conf["type"]
            slide_template_config = self.config["slide_types"][slide_type]
            slide_template = self.templates[slide_template_config["template_key"]]
            preprocess_fn = getattr(
                preprocess, slide_template_config["preprocess"]) if "preprocess" in slide_template_config else None
            element_conf = {"uuid": str(uuid.uuid1())}
            if preprocess_fn:
                _slide = preprocess_fn(slide_conf)
                element_conf.update(_slide)
            else:
                element_conf.update(slide_conf)
            element = slide_template.render(element_conf)
            final_slides.append({"element": element, "title": slide_title, "type": slide_conf.get(
                "type", ""), "element_config": element_conf})
        presentation = main_template.render(
            {"slides": final_slides, "title": unit_title})
        return presentation

    def assemble_h5p(self, content: dict[str, Any]) -> Buffer:
        pass
