import json
from typing import List, Optional, Dict, Any

from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class NewWaypoint(BaseModel):
    name: str
    floor: int
    keywords: List[str]
    aliases: Optional[List[str]]

class AddWaypointsInput(BaseModel):
    waypoints: List[NewWaypoint]
    waypoint_set: Optional[str]

class WaypointV1PostResponse(BaseModel):
    response : Dict[str, Any]

@router.post("/v1/waypoint")
def add_waypoints(body: AddWaypointsInput):
    """Add Waypoints Endpoint."""
    return WaypointV1PostResponse(response={"Response": "Success"})
