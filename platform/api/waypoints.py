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


class UpdateWaypointsInput(BaseModel):
    waypoints: List[NewWaypoint]
    waypoint_set: Optional[str]

class WaypointV1PutResponse(BaseModel):
    response : Dict[str, Any]

@router.put("/v1/waypoint")
def update_waypoints(body: UpdateWaypointsInput):
    """Update Waypoints Endpoint."""
    return WaypointV1PutResponse(response={"Response": "Success"})


class DeleteWaypointsInput(BaseModel):
    waypoints: List[NewWaypoint]
    waypoint_set: Optional[str]

class WaypointV1DeleteResponse(BaseModel):
    response : Dict[str, Any]

@router.delete("/v1/waypoint")
def delete_waypoints(body: DeleteWaypointsInput):
    """Delete Waypoints Endpoint."""
    return WaypointV1DeleteResponse(response={"Response": "Success"})
