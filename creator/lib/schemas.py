from typing import Any, List, Literal, Optional, TypedDict
from openai import BaseModel
from langchain_core.runnables.base import Runnable




# SLIDE MODALITIES

class Modality(BaseModel):
    id: Literal["text","drag_text","single_choice"]
    name:str    
    description: str

class Modality_(TypedDict):
    id: Literal["text","drag_text","single_choice"]
    name:str
    description: str

class Config(BaseModel):
    model: str
    temperature: float = 0.7
    instructions: str
    topic: str
    modalities: List[Modality]

class SystemConfigRequest(Config):
    preset_id:Optional[int|str] = None
    session_id:str


class ChatRequest(BaseModel):
    session_id: str
    msg: str

class Message(TypedDict):
    msg:str
    role:Literal["user","assistant"]


class Model(TypedDict):
    id:str
    name:str
    description:str
    created:int
    pricing:list[float]

class ConfigData(TypedDict):
    default_model_id:str
    models:list[Model]
    temperature:float
    topic:str
    instructions:str
    available_modalities: list[Modality_]

class SessionData(TypedDict):
    llm: Runnable
    initial_system_prompt: str
    config:SystemConfigRequest
    last_output:str
    last_output_parsed:dict[str,Any]
    feedback_history:List[Message]
    last_activity: float

class Feedback(BaseModel):
    text:str
    rating: str

    
class AuthRequest(BaseModel):
    access_token: str


class FeedbackRequest(BaseModel):
    session_id: str
    feedback: Feedback


## OPENROUTER MODEL DATA
#.........................................................


class Architecture(BaseModel):
    modality: str
    input_modalities: List[str]
    output_modalities: List[str]
    tokenizer: Optional[str] = None
    instruct_type: Optional[Any] = None

class Pricing(BaseModel):
    prompt: str
    completion: str
    request: Optional[str] = None
    image: Optional[str] = None
    audio: Optional[str] = None
    web_search: Optional[str] = None
    internal_reasoning: Optional[str] = None


class TopProvider(BaseModel):
    context_length: Optional[int] = None
    max_completion_tokens: Optional[int] = None
    is_moderated: Optional[bool] = None


class ModelItem(BaseModel):
    id: str
    name: str
    description: str
    canonical_slug: Optional[str] = None
    hugging_face_id: Optional[str] = None
    created: int
    context_length: Optional[int] = None
    architecture: Architecture
    pricing: Pricing
    top_provider: Optional[TopProvider] = None
    per_request_limits: Optional[Any] = None
    supported_parameters: Optional[List[str]] = None
