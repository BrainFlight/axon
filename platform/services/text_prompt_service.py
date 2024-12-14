import json
import logging

from inference.model_interface import ModelConfig, ModelInterface, ModelProvider
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

local_config = ModelConfig(
    provider=ModelProvider.LOCAL,
    model_name="distilbert/distilgpt2",
    additional_params={"task": "text-generation"},
)

local_interface = ModelInterface(local_config)

def text_prompt_service(input_prompt: str) -> str:
    """Text Prompt Service."""
    # response = local_interface.prompt(f"{PROMPT_V1}{input_prompt}")
    # response = json.loads(response)

    prompt = load_prompt_from_file("e7_v1_xrif_waypoints_keywords")

    response = prompt.render(query=input_prompt)

    logger.info(f"Response received: {response}")
    print(response)

    return response
