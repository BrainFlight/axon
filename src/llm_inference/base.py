from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field
from enum import Enum

from skills.skill_spec import Skill


class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    LOCAL = "local"
    CUSTOM = "custom"


@dataclass
class OutputFormat:
    format_type: str  # e.g., "json", "xml", "markdown"
    schema: Optional[Dict[str, Any]] = None
    additional_constraints: Optional[Dict[str, Any]] = None


@dataclass
class ModelConfig:
    provider: ModelProvider
    model_name: str
    api_key: Optional[str] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)
    supported_skills: Dict[str, Skill] = field(default_factory=dict)
    default_output_format: Optional[OutputFormat] = None


class LLMStrategy(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config
        self.active_skills: Dict[str, Skill] = {}
        self.current_output_format: Optional[OutputFormat] = (
            config.default_output_format
        )

    @abstractmethod
    def prompt(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def _format_prompt_with_skills(self, prompt: str) -> str:
        """Format the prompt to include active skills in provider-specific way"""
        pass

    @abstractmethod
    def _format_prompt_for_output(self, prompt: str) -> str:
        """Format the prompt to enforce output format in provider-specific way"""
        pass

    def add_skills(self, skill_names: List[str]) -> None:
        for skill_name in skill_names:
            if skill_name in self.config.supported_skills:
                self.active_skills[skill_name] = self.config.supported_skills[
                    skill_name
                ]
            else:
                raise ValueError(f"Skill {skill_name} not supported for this model")

    def remove_skills(self, skill_names: List[str]) -> None:
        for skill_name in skill_names:
            self.active_skills.pop(skill_name, None)

    def set_output_format(self, output_format: Union[OutputFormat, str]) -> None:
        if isinstance(output_format, str):
            self.current_output_format = OutputFormat(format_type=output_format)
        else:
            self.current_output_format = output_format
