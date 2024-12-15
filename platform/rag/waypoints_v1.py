from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from functools import lru_cache
import uuid

from db.db_client import DBClient

@dataclass
class Waypoint:
    id: uuid.UUID
    name: str
    floor: int
    keywords: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)

class WaypointRAG:
    def __init__(self):
        self._waypoints: Dict[str, Waypoint] = {}
        self._alias_map: Dict[str, str] = {}

    def load_waypoints(self, db_client: Optional[DBClient] = None, location_set: Optional[str] = None): # TODO: Update to include DB client
        """Initialize the waypoint system with all known locations from a database."""
        init_dict = {
            "E7 1st floor Elevators": Waypoint(
                id=uuid.uuid4(),
                name="E7 1st floor Elevators",
                floor=1,
                keywords=["entrance"],
            ),
            "E7 North Entrance": Waypoint(
                id=uuid.uuid4(),
                name="E7 North Entrance",
                floor=1,
                keywords=["entrance"],
            ),
            "E7 East Entrance": Waypoint(
                id=uuid.uuid4(),
                name="E7 East Entrance",
                floor=1,
                keywords=["entrance"],
            ),
            "E7 South Entrance": Waypoint(
                id=uuid.uuid4(),
                name="E7 South Entrance",
                floor=1,
                keywords=["entrance"],
            ),
            "E7 Coffee and Donuts": Waypoint(
                id=uuid.uuid4(),
                name="E7 Coffee and Donuts",
                floor=1,
                keywords=["food and drink", "snacks"],
                aliases=["CnD"]
            ),
            "Outreach Classroom": Waypoint(
                id=uuid.uuid4(),
                name="Outreach Classroom",
                floor=1,
                keywords=["classroom", "lecture hall"],
            ),
            "RoboHub Entrance": Waypoint(
                id=uuid.uuid4(),
                name="RoboHub Entrance",
                floor=1,
                keywords=["robots"],
            ),
            "Vending Machine": Waypoint(
                id=uuid.uuid4(),
                name="Vending Machine",
                floor=1,
                keywords=["food and drink", "snacks"],
            ),
            "Room 2106": Waypoint(
                id=uuid.uuid4(),
                name="Room 2106",
                floor=2,
                keywords=["office", "zach", "WEEF"],
            )
        }

        for waypoint, value in init_dict.items():
            self._waypoints[waypoint] = value

        for waypoint in self._waypoints.values():
            for alias in waypoint.aliases:
                self._alias_map[alias] = waypoint.name
    
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
    
    @lru_cache(maxsize=512)
    def get_waypoint_by_name_or_alias(self, query: str) -> Optional[Waypoint]:
        """Retrieve waypoint with caching."""
        if query in self._waypoints:
            return self._waypoints[query]
            
        if query in self._alias_map:
            return self._waypoints[self._alias_map[query]]
        
        return None
    
    @lru_cache(maxsize=1)
    def get_waypoints(self) -> str:
        """Get waypoint list."""
        waypoint_list = []
        
        for waypoint in self._waypoints.values():
            keywords = ', '.join(waypoint.keywords) if waypoint.keywords else "None"
            aliases = ', '.join(waypoint.aliases) if waypoint.aliases else "None"
            waypoint_list.append(
                f"- {waypoint.name}, floor: {waypoint.floor}, keywords: {keywords}, aliases: {aliases}"
            )
        
        return f"{chr(10).join(sorted(waypoint_list))}"
