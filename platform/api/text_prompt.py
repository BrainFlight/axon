from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter
from main import config
from inference.model_interface import ModelConfig, ModelInterface, ModelProvider


cohere_config = ModelConfig(
        provider=ModelProvider.COHERE,
        api_key=config.COHERE_API_KEY,
    )
    
cohere_interface = ModelInterface(cohere_config)

class prompt_body(BaseModel):
    model_name: str
    prompt: str
    prompt_args: Optional[dict]
    max_tokens: Optional[int]
    temperature: Optional[float]
    top_p: Optional[float]
    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]
    stop: Optional[List[str]]
    # load_to_cache: Optional[bool] = False

class api_response(BaseModel):
    response : str

router = APIRouter()

@router.post("/v1/text_prompt")
async def text_prompt_service(body: prompt_body):
    """Doc string"""
    # TODO: Validate input
    # response = text_prompt_service(body)
    response = cohere_interface.prompt(body.prompt)

    return api_response(response=response)


# from inference.model_interface import ModelConfig, ModelInterface, ModelProvider
# from config.config import GlobalConfig


# query1 = "Can you get a coffee to the robohub?"
# query2 = "get me an energy drink, I'm near the elevators on the 1st floor"

# prompt_v1 = """
# You control a robot that can navigate through a building based on a json instruction format, you understand several waypoints that have been given to you before (you can use RAG to retrieve what room numbers or waypoints correspond to which people or semantics).
# Here are all the waypoints you have access to (you must refer to them with these exact titles when generating the output format):
# - E7 1st floor Elevators, floor: 1
# - E7 North Entrance, floor: 1
# - E7 East Entrance, floor: 1
# - E7 South Entrance, floor: 1
# - E7 Coffee and Donuts, floor: 1
# - Outreach Classroom, floor: 1
# - RoboHub Entrance, floor: 1
# - Vending Machine, floor: 1
# - Room 2106, floor: 2

# Extra information:
# - Room 2106 is Zach's office
# - Coffee and Donuts can be referred to as CnD by students

# Example Prompt: Can you pick something up from Zach's office and drop it off at the RoboHub?

# Example Answer:
# {
#     "goals": [
#         {
#             "name": "Room 2106",
#             "floor": 1
#         },
#         {
#             "name": "RoboHub Entrance",
#             "floor": 1
#         }
#     ]
# }
# Prompt: 
# """

# config = GlobalConfig()

# cohere_config = ModelConfig(
#     provider=ModelProvider.COHERE,
#     model_name="cohere",
#     api_key=config.cohere_api_key,
# )
    
# cohere_interface = ModelInterface(cohere_config)
# print(cohere_interface.prompt(f"{prompt_v1} {query2}"))
