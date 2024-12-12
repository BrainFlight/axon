from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from functools import lru_cache
import uuid

@dataclass(frozen=True)
class Waypoint:
    """Immutable waypoint data structure."""
    id: uuid.UUID
    name: str
    floor: int
    keywords: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)

class WaypointRAG:
    def __init__(self):
        self._waypoints: Dict[str, Waypoint] = {}
        self._alias_map: Dict[str, str] = {}
        
    def initialize_waypoints(self, waypoints_list: List[Dict[str, Any]]):
        """Initialize the waypoint system with all known locations from a list of dictionaries."""
        for waypoint_data in waypoints_list:
            self.add_waypoint(
                name=waypoint_data["name"],
                floor=waypoint_data["floor"],
                keywords=waypoint_data.get("keywords", []),
                aliases=waypoint_data.get("aliases", [])
            )
            
    def add_waypoint(
        self, 
        name: str, 
        floor: int, 
        keywords: Optional[List[str]] = None, 
        aliases: Optional[List[str]] = None
    ) -> Waypoint:
        """Add a waypoint with all its properties."""
        waypoint = Waypoint(
            id=uuid.uuid4(),
            name=name,
            floor=floor,
            keywords=keywords or [],
            aliases=aliases or []
        )
        
        self._waypoints[name] = waypoint
        
        if aliases:
            for alias in aliases:
                self._alias_map[alias] = name
                
        return waypoint
    
    @lru_cache(maxsize=1024)
    def get_waypoint_by_name_or_alias(self, query: str) -> Optional[Waypoint]:
        """Retrieve waypoint with caching."""
        if query in self._waypoints:
            return self._waypoints[query]
            
        if query in self._alias_map:
            return self._waypoints[self._alias_map[query]]
        
        return None
    
    @lru_cache(maxsize=1)
    def generate_prompt_with_waypoints(self) -> str:
        """Generate prompt with cached waypoint list."""
        waypoint_list = [
            f"- {waypoint.name}, floor: {waypoint.floor}"
            for waypoint in self._waypoints.values()
        ]
        
        return f"""
            You control a robot that can navigate through a building based on a json instruction format, you understand several waypoints that have been given to you before (you can use RAG to retrieve what room numbers or waypoints correspond to which people or semantics).
            Here are all the waypoints you have access to (you must refer to them with these exact titles when generating the output format):
            {chr(10).join(sorted(waypoint_list))}

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

# Example usage
if __name__ == "__main__":
    # Example waypoints data (could be loaded from JSON file)
    waypoints_data = [
        {
            "name": "E7 1st floor Elevators",
            "floor": 1,
            "keywords": ["elevator", "lift"],
            "aliases": []
        },
        {
            "name": "E7 North Entrance",
            "floor": 1,
            "keywords": ["entrance", "door", "north"],
            "aliases": []
        },
        {
            "name": "E7 East Entrance",
            "floor": 1,
            "keywords": ["entrance", "door", "east"],
            "aliases": []
        },
        {
            "name": "E7 South Entrance",
            "floor": 1,
            "keywords": ["entrance", "door", "south"],
            "aliases": []
        },
        {
            "name": "E7 Coffee and Donuts",
            "floor": 1,
            "keywords": ["coffee", "food", "drinks"],
            "aliases": ["CnD"]
        },
        {
            "name": "Outreach Classroom",
            "floor": 1,
            "keywords": ["classroom", "teaching"],
            "aliases": []
        },
        {
            "name": "RoboHub Entrance",
            "floor": 1,
            "keywords": ["robots", "entrance"],
            "aliases": []
        },
        {
            "name": "Vending Machine",
            "floor": 1,
            "keywords": ["snacks", "drinks"],
            "aliases": []
        },
        {
            "name": "Room 2106",
            "floor": 2,
            "keywords": ["office", "workspace"],
            "aliases": ["Zach"]
        }
    ]
    
    rag = WaypointRAG()
    rag.initialize_waypoints(waypoints_data)
    
    cnd = rag.get_waypoint_by_name_or_alias("CnD")
    print(f"CnD lookup: {cnd}")
    print(f"CnD keywords: {cnd.keywords}")
    print(f"CnD UUID: {cnd.id}")
    