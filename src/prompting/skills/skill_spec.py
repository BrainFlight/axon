from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str
    parameters: Optional[Dict[str, Any]] = None
    provider_specific_config: Optional[Dict[str, Any]] = None
