"""
General assembler logic that can be configured via config.yml
"""
from contextlib import contextmanager
import importlib.util
from pathlib import Path
import shutil
import tempfile
from typing import Any
from warnings import warn
from jinja2 import Environment, FileSystemLoader
import uuid
from ..lib.loader import load_yaml
from ..lib.types import AssemblerConfig
from ..lib.zip_folder import load_zip_to_temp, remove_temp, zip_folder
from . import preprocess


BASE_PATH = Path(__file__).resolve(
).parent

DEFAULT_TEMPLATE_PATH = BASE_PATH / Path("resources/templates/default.zip")

try:
    temp_root = Path(tempfile.gettempdir())
    for temp_path in temp_root.glob("*unit_assembler"):
        try:
            shutil.rmtree(temp_path)
        except Exception:
            try:
                temp_path.unlink()
            except Exception as e:
                warn(str(e))
except Exception as e:
    warn(str(e))

class UnitAssembler:
    _config: AssemblerConfig | None = None
    _unit_template_path: Path | None = None
    _jinja_templates_path: Path | None = None

    @classmethod
    def set_config(cls, template_path: str | None = None, config: AssemblerConfig | dict[str, Any] = {}) -> None:
        cls._ensure_initialized(template_path=template_path, config=config)

    @classmethod
    def _ensure_initialized(cls, template_path: str | None = None, config: AssemblerConfig | dict[str, Any] | None = None) -> None:
        # cls.template_path = DEFAULT_TEMPLATE_PATH
        if template_path:
            cls.template_path  = load_zip_to_temp(str(template_path))
        else:
            cls.template_path  = load_zip_to_temp(str(DEFAULT_TEMPLATE_PATH))
        cls._unit_template_path = cls.template_path / Path("unit")
        cls._jinja_templates_path = cls.template_path / Path("jinja")
        cls._jinja_env = Environment(
            loader=FileSystemLoader(str(cls._jinja_templates_path))
        )
        cls._jinja_entry_point = cls._jinja_env.get_template("main.j2")

        if cls._config is not None and config is None:
            return

        cls._config = load_yaml(BASE_PATH / "config.yml")

        if config:
            cls._config.update(config)  # type: ignore


    @classmethod
    def assemble_content(cls, intermediate_content: dict[str, Any]) -> str:
        cls._ensure_initialized()
        if cls._config is None:
            raise RuntimeError("UnitAssembler is not initialized.")
        
        if not cls._jinja_templates_path:
            raise RuntimeError("No template path found.")
        final_slides = []

        # get unit tile for cover page
        unit_title = intermediate_content.get(
            "title", cls._config["defaults"]["unit_title"])

        # render slide content as elements
        for slide_conf in intermediate_content.get("slides", []):
            slide_type = slide_conf["type"]
            slide_template_config = cls._config["slide_types"][slide_type]
            element_conf = {"uuid": str(uuid.uuid1()), **slide_conf}

            preprocess_fn_name = slide_template_config.get("preprocess", None)
            if preprocess_fn_name:
                preprocess_fn = getattr(
                    preprocess, preprocess_fn_name)
                _slide = preprocess_fn(slide_conf)
                element_conf.update(_slide)
            else:
                element_conf.update(slide_conf)
            final_slides.append(element_conf)

        presentation_conf =  {"slides": final_slides, "title": unit_title}

        valid_path = cls.template_path / "valid.py"
        if valid_path:
            spec = importlib.util.spec_from_file_location("unit_template_valid", valid_path)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"Unable to load validator from {valid_path}.")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _validator = module.Main
            _validator(**presentation_conf)  # type: ignore[misc]

        # manufacture the final presentation
        presentation = cls._jinja_entry_point.render(**presentation_conf)
        return presentation

    @classmethod
    def assemble_h5p(cls, presentation: str, output_dir: str | Path = ".out", out_name: str = "unit.h5p", return_buffer=False):
        try:
            cls._ensure_initialized()
            if cls._unit_template_path is None:
                raise RuntimeError("UnitAssembler is not initialized.")

            contents = [{
                "filename": "content.json",
                "path": "content",
                "content": presentation
            }]
            zip_path = cls._unit_template_path
            buffer = zip_folder(str(zip_path), contents=contents)  # type: ignore
            if return_buffer:
                return buffer
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / out_name
            output_path.write_bytes(buffer)
            return output_path
        finally:
            remove_temp(cls.template_path)