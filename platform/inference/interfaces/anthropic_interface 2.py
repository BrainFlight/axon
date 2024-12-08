import logging

import anthropic

from inference.model_interface import LLMStrategy


def send_to_claude(client: anthropic.Anthropic, prompt: str):
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content
    except Exception as e:
        print(f"An error occurred while communicating with the Anthropic API: {e}")
        return None
    
class AnthropicStrategy(LLMStrategy):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
    
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
        return "Anthropic response"
