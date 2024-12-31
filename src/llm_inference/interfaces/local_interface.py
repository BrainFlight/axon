from rpc.local_inference import InferencePodClient
from llm_inference.base import LLMStrategy, ModelConfig


class LocalStrategy(LLMStrategy):
    def __init__(self, config: ModelConfig):
        self.config = config
        self._client = InferencePodClient(host="localhost", port=50051)

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

        # Configure the model
        task = self.config.additional_params.get("task", "sentiment-analysis")

        success, message = self._client.configure_model(
            model_name=self.config.model_name, task=task
        )
        print(f"Configuration: {message}")

        if success:
            output, confidence = self._client.run_inference(prompt)
            print(f"Output: {output}")
            print(f"Confidence: {confidence}")

            return output
        return "Error running inference"
