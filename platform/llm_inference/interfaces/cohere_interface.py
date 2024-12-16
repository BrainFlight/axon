import os
import sys

import cohere

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from llm_inference.base import LLMStrategy, ModelConfig


class CohereStrategy(LLMStrategy):
    def __init__(self, config: ModelConfig):
        self.config = config
        self._cohere_client = cohere.ClientV2(api_key=config.api_key)

    def _format_prompt_with_skills(self, prompt: str) -> str:
        return prompt

    def _format_prompt_for_output(self, prompt: str) -> str:
        return prompt
    
    def _get_skills(self) -> str | None:
        """Get Skills for Cohere Model."""
        if not self.config.supported_skills:
            return None
        
        skill_descriptions = [
            f"- {skill.name}: {skill.description}"
            for skill in self.config.supported_skills.values()
        ]
        
        return f"Using the following skills:\n{''.join(skill_descriptions)}"


    def prompt(self, prompt: str, **kwargs) -> str:
        """Prompt a Cohere Model."""
        if kwargs.get("model_name"):
            model_name = kwargs["model_name"]
        else:
            model_name = "command-r-plus-08-2024"

        if kwargs.get("structured_output"):
            structured_output = kwargs["structured_output"]
    
            response = self._cohere_client.chat(
                model=model_name,
                messages=[
                    {
                        "role" : "user", 
                        "content" : prompt
                    }
                ],
                response_format=structured_output,
            )
            return response.message.content[0].text
        else:
            response = self._cohere_client.chat(
                model=model_name,
                messages=[
                    {
                        "role" : "user", 
                        "content" : prompt
                    }
                ]
            )
            return response.message.content[0].text
