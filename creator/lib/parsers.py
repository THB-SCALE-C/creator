from typing import Any, Tuple
from jinja2 import Template
from langchain_core.output_parsers import JsonOutputParser
from supabase import Client


def trim_json_string(text: str) -> Tuple[str,str]:
    """
    Cuts the JSON out of string response, if it is the last element in the string, and returns a tuple of the prefixed content and the JSON.
    """
    marker = "```json"
    marker_alt = "{\n"
    marker_idx = s if (s:=text.find(marker)) != -1 else text.find(marker_alt)
    if marker_idx == -1:
        return text,"{}"
    return text[:marker_idx].strip(), text[marker_idx:].strip().replace("```","").replace("json","")

def trim_and_parse(text:str) -> dict[str,Any]:
    _, trimmed = trim_json_string(text)
    return JsonOutputParser().parse(trimmed)

def render_and_parse_template(template:Template, context:dict) -> dict:
    """
    Renders a template with the given context and returns the parsed JSON.
    """
    rendered = template.render(context)
    parser = JsonOutputParser()
    return parser.parse(rendered)




