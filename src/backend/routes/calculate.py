from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import numpy as np
import math

# Define a router
router = APIRouter()


@router.post("/calculate")
def calculate(
    mortar_easting: float,
    mortar_northing: float,
    observer_easting: float,
    observer_northing: float,
    obs_to_enemy_azimuth: float,
    obs_to_enemy_distance: float,
):
    azimuth, distance = azimuth_from_observer_relative(
        mortar_easting,
        mortar_northing,
        observer_easting,
        observer_northing,
        obs_to_enemy_azimuth,
        obs_to_enemy_distance,
    )
    return {"azimuth": round(azimuth, 2), "distance": round(distance, 2)}


@router.post("/calculate2")
def calculate2(
    mortar_easting: float,
    mortar_northing: float,
    enemy_easting: float,
    enemy_northing: float,
):
    distance = distancefunc(
        mortar_easting, mortar_northing, enemy_easting, enemy_northing
    )
    azimuth = azimuth_from_grids(
        mortar_easting, mortar_northing, enemy_easting, enemy_northing
    )
    return {"azimuth": round(azimuth, 2), "distance": round(distance, 2)}


# upper_half determine if the user wants to raise or low the elevation from
# 45 degrees to reach target (mortar vs howitzer)
@router.post("/calculate3")
def calculate_elevation(initial_velocity: float, target_height: float, distance: float, upper_half: bool):
    current_elevation = 45.
    # Check if target is even reachable using optimal launch angle
    current_distance = ballistic_sim3(
        initial_velocity, current_elevation, target_height, 0.001
    )[0]
    if current_distance < distance:
        # target unreachable
        return HTMLResponse("Target Unreachable.", status_code=400)
    while current_distance - distance > 0.1:
        if upper_half:
            current_elevation = current_elevation + 0.01
        else:
            current_elevation = current_elevation - 0.01
        current_distance = ballistic_sim3(
            initial_velocity, current_elevation, target_height, 0.001
        )[0]
    return {
        "elevation": round(math.radians(current_elevation) * 1000, 0),
        "time_to_impact": round(ballistic_sim3(
            initial_velocity, current_elevation, target_height, 0.001
        )[1], 1),
    }


def ballistic_sim(initial_velocity, elevation, target_height, delta_t):
    t = 0
    x = 0
    y = 0
    v_0 = math.sin(math.radians(elevation)) * initial_velocity
    v_y = math.sin(math.radians(elevation)) * initial_velocity
    v_x = math.cos(math.radians(elevation)) * initial_velocity
    while v_y > 0 or y > target_height:
        t = t + delta_t
        x = x + v_x * delta_t
        y = y + v_y * delta_t
        v_y = v_0 - 9.81 * t
    return x, t


def ballistic_sim2(initial_velocity, elevation, target_height, delta_t):
    f = .00031  # from arma for 81mm
    t = 0
    x = 0
    y = 0
    v_y = math.sin(math.radians(elevation)) * initial_velocity
    v_x = math.cos(math.radians(elevation)) * initial_velocity
    while (v_y > 0 or y > target_height):
        v = math.sqrt(v_x ** 2 + v_y ** 2)
        deceleration = f * v ** 2
        v_theta = math.atan(v_y / v_x)
        # decel_x = -1 * math.cos(v_theta) * deceleration
        # decel_y = -1 * math.sin(v_theta) * deceleration
        decel_x = -1 * deceleration
        decel_y = -1 * deceleration
        decel_y = decel_y - 9.81
        
        t = t + delta_t
        x = x + v_x * delta_t
        y = y + v_y * delta_t
        v_x = v_x + (decel_x * delta_t)
        v_y = v_y + (decel_y * delta_t)
    return x, t


def ballistic_sim3(initial_velocity, elevation, target_height, delta_t):
    f = -.00031  # from arma for 81mm
    t = 0
    position = np.array([0, 0])
    gravity = np.array([0, -9.81])
    velocity = initial_velocity * np.array([math.cos(math.radians(elevation)), math.sin(math.radians(elevation))])
    while (velocity[1] > 0 or position[1] > target_height):
        position = position + velocity * delta_t

        speed = np.linalg.norm(velocity)
        acceleration = (velocity * speed * f) + gravity

        velocity = velocity + acceleration * delta_t
        t = t + delta_t
    return position[0], t


# FIXME: Not taking into account relative height from observer, which means I'm
# calculating eastings/northings based on hypotenuse of the triangle rather
# than the actual x/y distance
def azimuth_from_observer_relative(
    mortar_easting: float,
    mortar_northing: float,
    observer_easting: float,
    observer_northing: float,
    obs_to_enemy_azimuth: float,
    obs_to_enemy_distance: float,
):
    # First need to calculate easting and northing of enemy
    # relative to observer
    obs_to_enemy_easting = 0.0
    obs_to_enemy_northing = 0.0

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
        obs_to_enemy_northing = (
            -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
        )
    # Due South
    elif obs_to_enemy_azimuth == 180:
        obs_to_enemy_easting = 0
        obs_to_enemy_northing = -1 * obs_to_enemy_distance

    # Third Quadrant
    elif obs_to_enemy_azimuth < 270:
        angle = 270 - obs_to_enemy_azimuth
        obs_to_enemy_easting = (
            -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        )
        obs_to_enemy_northing = (
            -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
        )
    # Due West
    elif obs_to_enemy_azimuth == 270:
        obs_to_enemy_easting = -1 * obs_to_enemy_distance
        obs_to_enemy_northing = 0
    # Fourth Quadrant
    else:
        angle = obs_to_enemy_azimuth - 270
        obs_to_enemy_easting = (
            -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        )
        obs_to_enemy_northing = math.sin(math.radians(angle)) * obs_to_enemy_distance

    enemy_easting = observer_easting + obs_to_enemy_easting
    enemy_northing = observer_northing + obs_to_enemy_northing

    distance = distancefunc(
        mortar_easting, mortar_northing, enemy_easting, enemy_northing
    )

    return (
        azimuth_from_grids(
            mortar_easting, mortar_northing, enemy_easting, enemy_northing
        ),
        distance,
    )


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


def enemy_pos_from_observer_relative(
    mortar_easting,
    mortar_northing,
    observer_easting,
    observer_northing,
    obs_to_enemy_azimuth,
    obs_to_enemy_distance,
):
    # First need to calculate easting and northing of enemy
    # relative to observer
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
        obs_to_enemy_northing = (
            -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
        )
    # Due South
    elif obs_to_enemy_azimuth == 180:
        obs_to_enemy_easting = 0
        obs_to_enemy_northing = -1 * obs_to_enemy_distance

    # Third Quadrant
    elif obs_to_enemy_azimuth < 270:
        angle = 270 - obs_to_enemy_azimuth
        obs_to_enemy_easting = (
            -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        )
        obs_to_enemy_northing = (
            -1 * math.sin(math.radians(angle)) * obs_to_enemy_distance
        )
    # Due West
    elif obs_to_enemy_azimuth == 270:
        obs_to_enemy_easting = -1 * obs_to_enemy_distance
        obs_to_enemy_northing = 0
    # Fourth Quadrant
    else:
        angle = obs_to_enemy_azimuth - 270
        obs_to_enemy_easting = (
            -1 * math.cos(math.radians(angle)) * obs_to_enemy_distance
        )
        obs_to_enemy_northing = math.sin(math.radians(angle)) * obs_to_enemy_distance

    enemy_easting = observer_easting + obs_to_enemy_easting
    enemy_northing = observer_northing + obs_to_enemy_northing
    return enemy_easting, enemy_northing
