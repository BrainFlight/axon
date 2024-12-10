import os
import sys

import cohere

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from inference.base import LLMStrategy, ModelConfig


class CohereStrategy(LLMStrategy):
    def __init__(self, config: ModelConfig):
        self.config = config
        self._cohere_client = cohere.ClientV2(api_key=config.api_key)
    
    def _format_prompt_with_skills(self, prompt: str) -> str:
        if not self.config.supported_skills:
            return prompt
        
        # Anthropic-specific implementation using natural language
        skill_descriptions = [
            f"- {skill.name}: {skill.description}"
            for skill in self.config.supported_skills.values()
        ]
        
        return f"Using the following capabilities:\n{''.join(skill_descriptions)}\n\n{prompt}"

    def _format_prompt_for_output(self, prompt: str) -> str:
        if not self.config.default_output_format:
            return prompt
            
        # Anthropic-specific output formatting using natural language
        if self.current_output_format.format_type == "json":
            return f"{prompt}\nProvide your response in valid JSON format."
        return prompt

    def prompt(self, prompt: str, **kwargs) -> str:
        formatted_prompt = self._format_prompt_with_skills(prompt)
        formatted_prompt = self._format_prompt_for_output(formatted_prompt)

        if kwargs.get("model_name"):
            model_name = kwargs["model_name"]
        else:
            model_name = "command-r-plus-08-2024"
        
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
