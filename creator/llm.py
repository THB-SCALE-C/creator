"""This is for now part of the creator -- to be capsulated soon..."""

import os
from dotenv import load_dotenv
from dspy import LM

load_dotenv()
KEY = os.getenv("OPENROUTER_API_KEY")


OPENROUTER_DSPY_LM_CONFIG = {
    "temperature":0.5,
    "api_key":KEY,
    "api_base":"https://openrouter.ai/api/v1"
}


def create_openrouter_lm(model="openai/gpt-oss-120b",key:None|str=None,**kwargs):
    if not KEY:
        if not key:
            raise ValueError("API Key for Openrouter is missing.")
        OPENROUTER_DSPY_LM_CONFIG["api_key"] = key
    return LM(**OPENROUTER_DSPY_LM_CONFIG, model=f"openrouter/{model}", **kwargs) 