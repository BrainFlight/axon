import json
import yaml
import logging
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import jinja2

from prompting.rag.fill import FILL_PARAMS
from db.cache import CacheClient
from db.db_client import DBClient

logger = logging.getLogger(__name__)


@dataclass
class Prompt:
    prompt_name: str
    prompt: str
    parameters: Dict[str, Any]
    rag: Dict[str, str]  # NOTE: {"<parameter_name>": "<rag_fill_name>"}
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
                    raise ValueError(
                        f"RAG fill function '{rag_fill_name}' not found in FILL_PARAMS"
                    )

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
    # TODO: Implement error handling (try/catch)
    with open(file_path, "r") as file:
        prompts_yaml = yaml.safe_load(file)

    return Prompt(
        prompt_name=prompt_name,
        prompt=prompts_yaml[prompt_name]["prompt"],
        parameters=prompts_yaml[prompt_name]["parameters"],
        rag=prompts_yaml[prompt_name]["rag"],
        metadata={},
    )


def purge_prompt_cache(prompt_name: str, cache: Optional[CacheClient] = None):
    """
    Purge both LRU and Redis caches for a prompt.
    """
    load_prompt_by_name.cache_clear()  # Clear LRU cache
    if cache:
        cache.delete(prompt_name)  # Clear Redis cache


@lru_cache(maxsize=128)
def load_prompt_by_name(
    prompt_name: str,
    db_client: DBClient = None,  # TODO: Add DBClient
    cache: Optional[CacheClient] = None,
) -> Optional[Prompt]:
    """
    Load prompts from database by name with local LRU and Redis caching.

    Args:
        prompt_name: Name of the prompt
        cache: Optional Redis cache client

    Returns:
        Prompt object if found, None if not found
    """
    try:
        # Try Redis first if available
        if cache:
            cached_prompt = cache.get(prompt_name)
            if cached_prompt:
                return Prompt(**json.loads(cached_prompt))

        # Load from database
        prompt_data = ""  # TODO: Load prompt from database
        if not prompt_data:
            return None

        prompt = Prompt(**prompt_data)

        # Update Redis cache if available
        if cache:
            cache.set(
                prompt_name,
                json.dumps(prompt.__dict__),
                ex=3600 * 5,  # 5 hour TTL
            )

        return prompt

    except Exception as e:
        # Log error
        print(f"Error loading prompt {prompt_name}: {e}")
        return None


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
