import json
import os
from typing import Any, List, Optional
from langchain_openai import ChatOpenAI
from pydantic import SecretStr, ValidationError
from langchain.messages import SystemMessage

from .utils.logger import setup_logger
from .utils.zip_folder import zip_folder

from .output_validation.slides import ParsedResponseModel
from .templating import forge_json_output_schema, forge_system_prompt, parse_model_response
from .utils.parsers import trim_and_parse
from .utils.schemas import Modality

# Environment configuration
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY") or ""
OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL") or ""


def create(model_props: dict[str, Any], prompt_props: dict[str, Any], prompt_template="system_base", logger=setup_logger(), openrouter_api_key=OPENROUTER_API_KEY, openrouter_base_url=OPENROUTER_BASE_URL):

    modalities: List[Modality] | None = prompt_props.get("modalities")
    output_schema = forge_json_output_schema(
        modalities) if modalities else None

    if output_schema:
        logger.debug(f"OUTPUT SCHEMA:\n{output_schema[:500]}\n{50*"*"}")

    system_prompt = forge_system_prompt(
        config={
            **prompt_props,
            "output_schema": output_schema,
        },
        template=prompt_template
    )
    system_msg = SystemMessage(content=system_prompt)
    logger.debug(f"PROMPT:\n{system_prompt[:500]}\n{50*"*"}")

    llm = _build_llm(openrouter_api_key,openrouter_base_url,**model_props)

    initial_response = llm.invoke([system_msg,]).content
    logger.debug(f"RESPONSE:\n{initial_response}\n{50*"*"}")
    parsed_response = trim_and_parse(str(initial_response))

    error = _validate_parsed_response(parsed_response)

    return initial_response, parsed_response, system_prompt, error


def manufacture_h5p(content: dict[str, Any], unit_title="unit"):
    content_json = parse_model_response(content)

    # Manipulate h5p.json for title
    with open(".out/h5p.json", encoding="utf-8") as f:
        h5p_json = json.load(f)
        h5p_json["title"] = unit_title
    buffer = zip_folder(".out/Unit", [
        {"path": "content", "filename": "content.json", "content": content_json},
        {"path": "", "filename": "h5p.json",
            "content": json.dumps(h5p_json, ensure_ascii=False)},
    ])
    return buffer


# Internal helpers (no API contract changes)
def _build_llm(key, url,**keys) -> ChatOpenAI:
    return ChatOpenAI(
        **keys,
        base_url=url,
        api_key=SecretStr(key),
    )


def _validate_parsed_response(parsed: dict) -> Exception|None:
    try:
        ParsedResponseModel.model_validate(parsed)
        return None
    except ValidationError as e:
        return e
