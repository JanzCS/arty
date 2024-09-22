from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.artillery_lib import (
    Artillery,
    GridCoord,
    azimuth_from_grids,
    azimuth_from_observer_relative,
    calculate_elevation,
    distancefunc,
)

# Map artillery string to Artillery object
artillery_mapping = {
    "m252": Artillery("m252", 0.25, 0.00031, 375, True),
    "m119": Artillery("m119", 23, 0.0043, 212.5, False),
    "t2s1": Artillery("t2s1", 21.76, 0.00647, 690, False),
}

# Define a router
router = APIRouter()


class GridCalculationRequest(BaseModel):
    mortar_easting: int
    mortar_northing: int
    mortar_height: int
    observer_to_enemy_azimuth: int
    enemy_easting: int
    enemy_northing: int
    enemy_height: int
    artillery: str


class PolarCalculationRequest(BaseModel):
    mortar_easting: int
    mortar_northing: int
    mortar_height: int
    observer_easting: int
    observer_northing: int
    observer_height: int
    observer_to_enemy_azimuth: int
    observer_to_enemy_horizontal: int
    observer_to_enemy_vertical: int
    artillery: str


@router.post("/calculate_elevation_polar")
def calculate_elevation_polar_endpoint(request: PolarCalculationRequest):
    artillery = artillery_mapping.get(request.artillery)
    if not artillery:
        raise HTTPException(status_code=400, detail="Invalid artillery type.")

    mortar_pos = GridCoord(request.mortar_easting, request.mortar_northing)
    obs_pos = GridCoord(request.observer_easting, request.observer_northing)

    afor_result = azimuth_from_observer_relative(
        mortar_pos,
        obs_pos,
        request.observer_to_enemy_azimuth,
        request.observer_to_enemy_horizontal,
    )
    mortar_to_enemy_azimuth = afor_result[0]
    mortar_to_enemy_distance = afor_result[1]

    ce_result = calculate_elevation(
        artillery,
        request.observer_height
        + request.observer_to_enemy_vertical
        - request.mortar_height,
        mortar_to_enemy_distance,
    )

    result = {
        "azimuth": round(mortar_to_enemy_azimuth, 2),
        "elevation": round(ce_result["elevation"], 0),
        "time_to_impact": ce_result["time_to_impact"],
        "max_ord": ce_result["max_ord"]
    }

    if isinstance(result, str):
        # If the result is an error message
        raise HTTPException(status_code=400, detail=result)
    else:
        return result


@router.post("/calculate_elevation_grid")
def calculate_elevation_grid_endpoint(request: GridCalculationRequest):
    artillery = artillery_mapping.get(request.artillery)
    if not artillery:
        raise HTTPException(status_code=400, detail="Invalid artillery type.")

    mortar_pos = GridCoord(request.mortar_easting, request.mortar_northing)
    enemy_pos = GridCoord(request.enemy_easting, request.enemy_northing)
    m2e_azimuth = azimuth_from_grids(mortar_pos, enemy_pos)
    m2e_horiz_distance = distancefunc(
        mortar_pos.easting,
        mortar_pos.northing,
        0,
        enemy_pos.easting,
        enemy_pos.northing,
        0,
    )
    ce_result = calculate_elevation(artillery, request.enemy_height,
                                    m2e_horiz_distance)
    result = {
        "azimuth": round(m2e_azimuth, 2),
        "elevation": round(ce_result["elevation"], 0),
        "time_to_impact": ce_result["time_to_impact"],
        "max_ord": ce_result["max_ord"]
    }

    if isinstance(result, str):
        # If the result is an error message
        raise HTTPException(status_code=400, detail=result)
    else:
        return result
