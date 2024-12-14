import json
import yaml
import logging
import uuid
from dataclasses import dataclass
from typing import Dict, Any
from pathlib import Path
import jinja2

from rag.fill import FILL_PARAMS

logger = logging.getLogger(__name__)


@dataclass
class Prompt:
    prompt_name: str
    prompt: str
    parameters: Dict[str, Any]
    rag: Dict[str, str] # NOTE: {"<parameter_name>": "<rag_fill_name>"}
    metadata: Dict[str, Any]

    # TODO: Will need these parameters later on:
    # prompt_id: uuid.UUID
    # version: str
    # created_at: str
    # updated_at: str

    def render(self, **kwargs) -> str:
        """
        Render the prompt template with provided parameters and execute RAG fills.
        
        Args:
            **kwargs: Parameter values for template rendering
            
        Returns:
            str: Rendered prompt with all parameters filled
            
        Raises:
            ValueError: If required parameters are missing or RAG fill function not found
        """
        for param_name, rag_fill_name in self.rag.items():
            if param_name not in kwargs:
                if rag_fill_name not in FILL_PARAMS:
                    raise ValueError(f"RAG fill function '{rag_fill_name}' not found in FILL_PARAMS")
                
                fill_func = FILL_PARAMS[rag_fill_name]
                kwargs[param_name] = fill_func()
        
        missing_params = set(self.parameters.keys()) - set(kwargs.keys())
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")
        
        template = jinja2.Template(self.prompt)
        return template.render(**kwargs)

def load_prompt_from_file(prompt_name: str, file_path: Path) -> Prompt:
    """
    Load prompts from a local YAML file.
    
    Args:
        file_path (Path): Path to the YAML file containing prompts
        
    Returns:
        Prompt: Prompt object
    """
    with open(file_path, 'r') as file:
        prompts_yaml = yaml.safe_load(file)
    
    return Prompt(
        prompt_name=prompt_name,
        prompt=prompts_yaml[prompt_name]['prompt'],
        parameters=prompts_yaml[prompt_name]['parameters'],
        rag=prompts_yaml[prompt_name]['rag'],
        metadata={}
    )

def load_prompt_by_name(prompt_name: str) -> Prompt:
    """
    Load prompts from database by name.
    
    Args:
        prompt_name (str): Name of the prompt
        
    Returns:
        Prompt: Prompt object
    """
    pass

def load_prompt_by_id(prompt_id: uuid.UUID) -> Prompt:
    """
    Load prompts from database by ID.
    
    Args:
        prompt_name (str): Name of the prompt
        
    Returns:
        Prompt: Prompt object
    """
    pass

def store_prompt(prompt: Prompt) -> bool:
    """
    Store a prompt in the database.

    Args:
        prompt (Prompt): Prompt object

    Returns:
        bool: True if successful, False otherwise
    """ 
    pass
