import logging

from openai import OpenAI

from inference.model_interface import LLMStrategy


def send_to_gpt4(client: OpenAI, prompt: str, model_name: str = "gpt-4o-mini"):
    try:
        # logger.info(f'prompt: {text}')
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model=model_name,
        )
        return(response)
    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        return None
    

class OpenAIStrategy(LLMStrategy):
    def _format_prompt_with_skills(self, prompt: str) -> str:
        if not self.active_skills:
            return prompt
        
        # OpenAI-specific implementation using function calling
        functions = [
            {
                "name": skill.name,
                "description": skill.description,
                "parameters": skill.parameters or {}
            }
            for skill in self.active_skills.values()
        ]
        
        return f"Using the following functions: {functions}\n{prompt}"

    def _format_prompt_for_output(self, prompt: str) -> str:
        if not self.current_output_format:
            return prompt
            
        # OpenAI-specific output formatting using function calling or response format
        if self.current_output_format.format_type == "json":
            return f"{prompt}\nRespond using JSON format."
        return prompt

    def prompt(self, prompt: str, **kwargs) -> str:
        formatted_prompt = self._format_prompt_with_skills(prompt)
        formatted_prompt = self._format_prompt_for_output(formatted_prompt)
        # Implement OpenAI-specific API call here
        return "OpenAI response"
