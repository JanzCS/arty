from fastapi import APIRouter
from pydantic import BaseModel
import math

# Define a router
router = APIRouter()

@router.post("/calculate")
def calculate(mortar_easting: float, mortar_northing: float, observer_easting: float, observer_northing: float, obs_to_enemy_azimuth: float, obs_to_enemy_distance: float):
    azimuth, distance = azimuth_from_observer_relative(mortar_easting, mortar_northing, observer_easting, observer_northing, obs_to_enemy_azimuth, obs_to_enemy_distance)
    return {"azimuth": round(azimuth, 2), "distance": round(distance, 2)}

@router.post("/calculate2")
def calculate2(mortar_easting: float, mortar_northing: float, enemy_easting: float, enemy_northing: float):
    distance = distancefunc(mortar_easting, mortar_northing, enemy_easting, enemy_northing)
    azimuth = azimuth_from_grids(mortar_easting, mortar_northing, enemy_easting, enemy_northing)
    return {"azimuth": round(azimuth, 2), "distance": round(distance, 2)}

def azimuth_from_observer_relative(mortar_easting: float, mortar_northing: float, observer_easting: float, observer_northing: float, obs_to_enemy_azimuth: float, obs_to_enemy_distance: float):
    # First need to calculate easting and northing of enemy relative to observer
    obs_to_enemy_easting = 0.
    obs_to_enemy_northing = 0.

    # Due North
    if obs_to_enemy_azimuth == 0:
        obs_to_enemy_easting = 0
        obs_to_enemy_northing = obs_to_enemy_distance
    # First Quadrant
    elif obs_to_enemy_azimuth < 90:
        angle = 90 - obs_to_enemy_azimuth
        obs_to_enemy_easting = math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = math.sin(math.radians(angle)) * obs_to_enemy_distance
    # Due East
    elif obs_to_enemy_azimuth == 90:
        obs_to_enemy_easting = obs_to_enemy_distance
        obs_to_enemy_northing = 0
    # Second Quadrant
    elif obs_to_enemy_azimuth < 180:
        angle = obs_to_enemy_azimuth - 90
        obs_to_enemy_easting = math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
    # Due South
    elif obs_to_enemy_azimuth == 180:
        obs_to_enemy_easting = 0
        obs_to_enemy_northing = -1 * obs_to_enemy_distance
        
    # Third Quadrant
    elif obs_to_enemy_azimuth < 270:
        angle = 270 - obs_to_enemy_azimuth
        obs_to_enemy_easting = -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
    # Due West
    elif obs_to_enemy_azimuth == 270:
        obs_to_enemy_easting = -1 * obs_to_enemy_distance
        obs_to_enemy_northing = 0
    # Fourth Quadrant
    else:
        angle = obs_to_enemy_azimuth - 270
        obs_to_enemy_easting = -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = math.sin(math.radians(angle)) * obs_to_enemy_distance

    enemy_easting = observer_easting + obs_to_enemy_easting
    enemy_northing = observer_northing + obs_to_enemy_northing

    distance = distancefunc(mortar_easting, mortar_northing, enemy_easting, enemy_northing)

    return azimuth_from_grids(mortar_easting, mortar_northing, enemy_easting, enemy_northing), distance


def distancefunc(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))

def azimuth_from_grids(start_easting, start_northing, end_easting, end_northing):
    east_vector = end_easting - start_easting
    north_vector = end_northing - start_northing

    # since we want azimuth, we need to shift the axes
    # east becomes north, and north becomes west

    temp = north_vector
    north_vector = east_vector
    east_vector = temp
    

    initial = math.degrees(math.atan2(north_vector, east_vector))
    if initial < 0:
        initial = 360 + initial
    
    return initial

def enemy_pos_from_observer_relative(mortar_easting, mortar_northing, observer_easting, observer_northing, obs_to_enemy_azimuth, obs_to_enemy_distance):
    # First need to calculate easting and northing of enemy relative to observer
    obs_to_enemy_easting = 0
    obs_to_enemy_northing = 0

    # Due North
    if obs_to_enemy_azimuth == 0:
        obs_to_enemy_easting = 0
        obs_to_enemy_northing = obs_to_enemy_distance
    # First Quadrant
    elif obs_to_enemy_azimuth < 90:
        angle = 90 - obs_to_enemy_azimuth
        obs_to_enemy_easting = math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = math.sin(math.radians(angle)) * obs_to_enemy_distance
    # Due East
    elif obs_to_enemy_azimuth == 90:
        obs_to_enemy_easting = obs_to_enemy_distance
        obs_to_enemy_northing = 0
    # Second Quadrant
    elif obs_to_enemy_azimuth < 180:
        angle = obs_to_enemy_azimuth - 90
        obs_to_enemy_easting = math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
    # Due South
    elif obs_to_enemy_azimuth == 180:
        obs_to_enemy_easting = 0
        obs_to_enemy_northing = -1 * obs_to_enemy_distance
        
    # Third Quadrant
    elif obs_to_enemy_azimuth < 270:
        angle = 270 - obs_to_enemy_azimuth
        obs_to_enemy_easting = -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
    # Due West
    elif obs_to_enemy_azimuth == 270:
        obs_to_enemy_easting = -1 * obs_to_enemy_distance
        obs_to_enemy_northing = 0
    # Fourth Quadrant
    else:
        angle = obs_to_enemy_azimuth - 270
        obs_to_enemy_easting = -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        obs_to_enemy_northing = math.sin(math.radians(angle)) * obs_to_enemy_distance

    enemy_easting = observer_easting + obs_to_enemy_easting
    enemy_northing = observer_northing + obs_to_enemy_northing
    return enemy_easting, enemy_northing