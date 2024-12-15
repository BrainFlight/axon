import json
import logging

from pathlib import Path

from llm_inference.model_interface import ModelConfig, ModelInterface, ModelProvider
from config import GlobalConfig
from prompt.prompt import load_prompt_from_file

logger = logging.getLogger(__name__)

config = GlobalConfig()

cohere_config = ModelConfig(
    provider=ModelProvider.COHERE,
    model_name="cohere",
    api_key=config.cohere_api_key,
)

cohere_interface = ModelInterface(cohere_config)

default_local_config = ModelConfig(
    provider=ModelProvider.LOCAL,
    model_name="distilbert/distilgpt2",
    additional_params={"task": "text-generation"},
)

local_interface = ModelInterface(default_local_config)

loaded_models = {
    "cohere": cohere_interface,
    "local_default": local_interface,
}

def text_prompt_service(
    model_name: str, 
    prompt_format_name: str, # e7_v1_xrif_waypoints_keywords
    prompt_args: dict,
) -> str:
    """Text Prompt Service."""
    local_prompt_path = Path('../local_prompts.yaml')

    if model_name not in loaded_models.keys():
        return "Model not found"
    
    model = loaded_models[model_name]

    prompt = load_prompt_from_file(prompt_format_name, local_prompt_path)

    response = model.prompt(prompt.render(**prompt_args))

    logger.info(f"Response received: {response}")
    print(response)

    return response
