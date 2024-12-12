import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from functools import lru_cache
from collections import defaultdict
import uuid


@dataclass(frozen=True)
class Waypoint:
    id: uuid.UUID
    name: str
    floor: int
    keywords: List[str] = None
    aliases: List[str] = None

class WaypointRAG:
    def __init__(self):
        self._waypoints: Dict[str, Waypoint] = {}
        self._aliases: defaultdict = defaultdict(set)
        self._normalize_pattern = re.compile(r'[^a-z0-9\s]')
        self._floor_index: defaultdict = defaultdict(set)
        
    def _normalize_text(self, text: str) -> str:
        """Normalize text for consistent matching."""
        return self._normalize_pattern.sub('', text.lower())
    
    def add_waypoint(
            self, 
            name: str, 
            floor: int, 
            keywords: Optional[List[str]] = None,
            aliases: Optional[List[str]] = None
        ):
        """Add a waypoint with optimized indexing."""
        waypoint = Waypoint(name=name, floor=floor)
        normalized_name = self._normalize_text(name)
        
        self._waypoints[normalized_name] = waypoint
        self._floor_index[floor].add(normalized_name)
        
        if aliases:
            for alias in aliases:
                normalized_alias = self._normalize_text(alias)
                self._aliases[normalized_alias].add(normalized_name)
                
    @lru_cache(maxsize=1024)
    def get_waypoint_by_name_or_alias(self, query: str) -> Optional[Waypoint]:
        """Cached waypoint retrieval with normalized matching."""
        normalized_query = self._normalize_text(query)
        
        # Direct lookup
        if normalized_query in self._waypoints:
            return self._waypoints[normalized_query]
            
        # Alias lookup
        if normalized_query in self._aliases:
            for waypoint_name in self._aliases[normalized_query]:
                return self._waypoints[waypoint_name]
        
        return None
    
    @lru_cache(maxsize=128)
    def get_waypoints_by_floor(self, floor: int) -> List[Waypoint]:
        """Cached retrieval of all waypoints on a specific floor."""
        return [self._waypoints[name] for name in self._floor_index[floor]]
    
    def generate_prompt_with_waypoints(self) -> str:
        """Generate prompt with cached waypoint list."""
        return self._generate_prompt_template(self._get_waypoint_list())
    
    @lru_cache(maxsize=1)
    def _get_waypoint_list(self) -> str:
        """Cache the waypoint list since it rarely changes."""
        waypoint_list = []
        for waypoint in self._waypoints.values():
            waypoint_list.append(f"- {waypoint.name}, floor: {waypoint.floor}")
        return '\n'.join(sorted(waypoint_list))
    
    @staticmethod
    def _generate_prompt_template(waypoint_list: str) -> str:
        """Static prompt template generation."""
        return f"""You control a robot that can navigate through a building based on a json instruction format, you understand several waypoints that have been given to you before (you can use RAG to retrieve what room numbers or waypoints correspond to which people or semantics).
        Here are all the waypoints you have access to (you must refer to them with these exact titles when generating the output format):
        {waypoint_list}

        Extra information:
        - Room 2106 is Zach's office
        - Coffee and Donuts can be referred to as CnD by students

        Example Prompt: Can you pick something up from Zach's office and drop it off at the RoboHub?

        Example Answer:
        {{
            "goals": [
                {{
                    "name": "Room 2106",
                    "floor": 1
                }},
                {{
                    "name": "RoboHub Entrance",
                    "floor": 1
                }}
            ]
        }}
        """

# Optimized initialization
def initialize_waypoints() -> WaypointRAG:
    """Initialize the waypoint system with all known locations."""
    rag = WaypointRAG()
    
    # Use a tuple for memory efficiency
    waypoints_data = (
        ("E7 1st floor Elevators", 1, None),
        ("E7 North Entrance", 1, None),
        ("E7 East Entrance", 1, None),
        ("E7 South Entrance", 1, None),
        ("E7 Coffee and Donuts", 1, ["CnD"]),
        ("Outreach Classroom", 1, None),
        ("RoboHub Entrance", 1, None),
        ("Vending Machine", 1, None),
        ("Room 2106", 2, ["Zach's office"])
    )
    
    for name, floor, aliases in waypoints_data:
        rag.add_waypoint(name, floor, aliases)
    
    return rag
