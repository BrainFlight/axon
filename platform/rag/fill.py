from typing import Dict, Callable

from rag.waypoints_v1 import WaypointRAG

waypoints = WaypointRAG()
waypoints.load_waypoints()

FILL_PARAMS: Dict[str, Callable] = {
    'get_waypoints': waypoints.get_waypoints,
}
