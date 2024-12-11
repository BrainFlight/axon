import logging
from typing import List, Union

# from inference.interfaces.openai_interface import OpenAIStrategy
# from inference.interfaces.anthropic_interface import AnthropicStrategy
from inference.interfaces.cohere_interface import CohereStrategy
from inference.interfaces.local_interface import LocalStrategy
from inference.base import LLMStrategy, ModelProvider, ModelConfig, OutputFormat
from skills.skill_spec import Skill

logger = logging.getLogger(__name__)

    
class ModelStrategyFactory:
    """
    Example of registering a custom strategy:

    class MyCustomStrategy(LLMStrategy):
        pass
    
    ModelStrategyFactory.register_strategy(ModelProvider.LOCAL, MyCustomStrategy)
    """
    _strategies = {
        # ModelProvider.OPENAI: OpenAIStrategy,
        # ModelProvider.ANTHROPIC: AnthropicStrategy,
        ModelProvider.COHERE: CohereStrategy,
        ModelProvider.LOCAL: LocalStrategy,
    }

    @classmethod
    def register_strategy(cls, provider: ModelProvider, strategy_class: type[LLMStrategy]):
        """Register a new strategy for a provider"""
        cls._strategies[provider] = strategy_class

    @classmethod
    def create_strategy(cls, config: ModelConfig) -> LLMStrategy:
        """Create a strategy instance for the given configuration"""
        strategy_class = cls._strategies.get(config.provider)
        if not strategy_class:
            raise ValueError(f"Unsupported model provider: {config.provider}")
        
        return strategy_class(config)

class ModelInterface:
    def __init__(self, config: ModelConfig):
        self.strategy = ModelStrategyFactory.create_strategy(config)
    
    def prompt(self, prompt: str, **kwargs) -> str:
        return self.strategy.prompt(prompt, **kwargs)
    
    def add_skills(self, skills: List[str]) -> None:
        self.strategy.add_skills(skills)
    
    def remove_skills(self, skills: List[str]) -> None:
        self.strategy.remove_skills(skills)
    
    def set_output_format(self, output_format: Union[OutputFormat, str]) -> None:
        self.strategy.set_output_format(output_format)
    
    def update_config(self, new_config: ModelConfig) -> None:
        self.strategy = ModelStrategyFactory.create_strategy(new_config)


# class ModelInterface:
#     def __init__(
#             self,
#             interface_type: str,
#             model_name: str,
#             skills: Optional[List[str]],
#             output_format: Optional[str],
#         ):
#         '''Initialize new ModelInterface object.'''
#         interface_type = interface_type.lower()

#         if interface_type == "openai":
#             from inference.interfaces.openai_interface import send_to_gpt4
#             self.prompt_function: Callable[[type], str] | None = send_to_gpt4

#         elif interface_type == "anthropic":
#             from inference.interfaces.anthropic_interface import send_to_claude
#             claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
#             self.prompt_function: Callable[[type], str] | None = send_to_claude

#         elif interface_type == "cohere":
#             from inference.interfaces.cohere_interface import send_to_cohere
#             cohere_client = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
#             self.prompt_function: Callable[[type], str] | None = send_to_cohere

#         elif interface_type == "local":
#             from inference.interfaces.openai_interface import send_to_gpt4
#             self.prompt_function: Callable[[type], str] | None = send_to_gpt4

#         else:
#             raise ValueError(f"Interface type {interface_type} is not supported.")
        
#         self.interface_type = interface_type
#         self.model_name = model_name
#         self.skills = skills
#         self.output_format = output_format

#     def prompt(self, prompt: str, params: Optional[Dict[str, Any]]) -> str:
#         '''Send prompt to model and return response.'''
#         response_text = self.prompt_function(prompt, params)
#         logger.info(f"Response: {response_text}")
#         return response_text

#     def add_skills(self, skills: List[str]):
#         '''Add skills to model.'''
#         pass

#     def remove_skills(self, skills: List[str]):
#         '''Remove skills from model.'''
#         pass

#     def set_output_format(self, output_format: str):
#         '''Set output format for model.'''
#         pass

# # Example usage
# def example_usage():
#     # Define supported skills
#     code_skill = Skill(
#         name="code_generation",
#         description="Generate code in various programming languages",
#         parameters={"language": "string", "task": "string"}
#     )
    
#     math_skill = Skill(
#         name="math_solving",
#         description="Solve mathematical problems",
#         parameters={"problem": "string", "show_work": "boolean"}
#     )
    
#     # Configure and create OpenAI interface with skills
#     openai_config = ModelConfig(
#         provider=ModelProvider.OPENAI,
#         model_name="gpt-4",
#         api_key="your-api-key",
#         supported_skills={"code_generation": code_skill, "math_solving": math_skill},
#         default_output_format=OutputFormat(format_type="json")
#     )
    
#     model = ModelInterface(openai_config)
    
#     # Add specific skills
#     model.add_skills(["code_generation"])
    
#     # Set output format
#     model.set_output_format(OutputFormat(
#         format_type="json",
#         schema={"type": "object", "properties": {"code": {"type": "string"}}}
#     ))
    
#     # Make request
#     response = model.prompt("Write a Python function to calculate fibonacci numbers")
