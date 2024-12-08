import os

from dotenv import load_dotenv
import cohere

from inference.model_interface import LLMStrategy


load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "ilzS5TMrkTzpk4wkyo7AEwHyWmbEDKepsGRFzFkT")

co = cohere.ClientV2(api_key=COHERE_API_KEY)

def send_to_cohere(client: cohere.CLientV2, prompt: str, model_name: str = "command-r-plus-08-2024"):
    response = client.chat(
        model=model_name,
        messages=[
            {
                "role" : "user", 
                "content" : prompt
            }
        ]
    )
    return response.message.content[0].text

query1 = "Can you get a coffee to the robohub?"
query2 = "get me an energy drink, I'm near the elevators on the 1st floor"

prompt_v1 = """
You control a robot that can navigate through a building based on a json instruction format, you understand several waypoints that have been given to you before (you can use RAG to retrieve what room numbers or waypoints correspond to which people or semantics).
Here are all the waypoints you have access to (you must refer to them with these exact titles when generating the output format):
- E7 1st floor Elevators, floor: 1
- E7 North Entrance, floor: 1
- E7 East Entrance, floor: 1
- E7 South Entrance, floor: 1
- E7 Coffee and Donuts, floor: 1
- Outreach Classroom, floor: 1
- RoboHub Entrance, floor: 1
- Vending Machine, floor: 1
- Room 2106, floor: 2

Extra information:
- Room 2106 is Zach's office
- Coffee and Donuts can be referred to as CnD by students

Example Prompt: Can you pick something up from Zach's office and drop it off at the RoboHub?

Example Answer:
{
    "goals": [
        {
            "name": "Room 2106",
            "floor": 1
        },
        {
            "name": "RoboHub Entrance",
            "floor": 1
        }
    ]
}
Prompt: 
"""

prompt_v2 = """
Can you write me a json file that specifies an API with 3 endpoints: /users, /users/{id}, and /users/{id}/posts?
"""

import json
output = json.loads(send_to_cohere(co, f"{prompt_v1}{query2}", model_name="command-r-plus-08-2024"))
for i in output["goals"]:
    print(i["name"])


class AnthropicStrategy(LLMStrategy):
    def _format_prompt_with_skills(self, prompt: str) -> str:
        if not self.active_skills:
            return prompt
        
        # Anthropic-specific implementation using natural language
        skill_descriptions = [
            f"- {skill.name}: {skill.description}"
            for skill in self.active_skills.values()
        ]
        
        return f"Using the following capabilities:\n{''.join(skill_descriptions)}\n\n{prompt}"

    def _format_prompt_for_output(self, prompt: str) -> str:
        if not self.current_output_format:
            return prompt
            
        # Anthropic-specific output formatting using natural language
        if self.current_output_format.format_type == "json":
            return f"{prompt}\nProvide your response in valid JSON format."
        return prompt

    def prompt(self, prompt: str, **kwargs) -> str:
        formatted_prompt = self._format_prompt_with_skills(prompt)
        formatted_prompt = self._format_prompt_for_output(formatted_prompt)
        # Implement Anthropic-specific API call here
        return "Cohere response"
