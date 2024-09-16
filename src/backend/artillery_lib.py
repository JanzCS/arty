import math
import numpy as np


class Artillery:
    """Represents an artillery shell with specific mass, air drag coefficient, and initial velocity.
    Also contains a boolean to tell if this artillery is shot at a low angle or high angle.

    Attributes:
        mass (float): Mass of the artillery shell in kilograms.
        air_drag (float): Air drag coefficient.
        initial_velocity (float): Initial velocity of the shell in meters per second.
        high_angle (bool): Whether the artillery shoots > 45 deg or below
    """

    def __init__(self, mass, air_drag, initial_velocity, high_angle):
        self.mass = mass
        self.air_drag = air_drag
        self.initial_velocity = initial_velocity
        self.high_angle = high_angle


class GridCoord:
    """Represents a coordinate point in a grid system with easting and northing values.

    Attributes:
        easting (float): The easting coordinate value.
        northing (float): The northing coordinate value.
    """

    def __init__(self, easting: float, northing: float):
        self.easting = easting
        self.northing = northing


def deg2EL(degrees):
    """Converts degrees to mils elevation plus offset for m252 artillery.

    Args:
        degrees (float): Elevation angle in degrees.

    Returns:
        float: Elevation in mils + offset (converted from degrees).
    """
    return math.radians(degrees) * 1000 - 960


def distancefunc(x1, y1, z1, x2, y2, z2):
    """
    Computes the Euclidean distance between two points in 3D space.

    Args:
        x1, y1, z1 (float): Coordinates of the first point.
        x2, y2, z2 (float): Coordinates of the second point.

    Returns:
        float: Euclidean distance between the two points.
    """
    return math.sqrt(
        math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2) + math.pow((z2 - z1), 2)
    )


def rotate_point_clockwise(point, deg_rotation):
    """Rotates a point around the origin clockwise by a specified angle.

    Args:
        point (array-like): A 2D point represented as [x, y].
        deg_rotation (float): Rotation angle in degrees.

    Returns:
        numpy.ndarray: The rotated point coordinates.
    """
    rad_rotation = math.radians(deg_rotation)
    rotation_matrix = np.array(
        [
            [math.cos(rad_rotation), math.sin(rad_rotation)],
            [-math.sin(rad_rotation), math.cos(rad_rotation)],
        ]
    )
    return np.dot(rotation_matrix, point)


# Rotate around the centroid of the polygon (average of all points)
def rotate_polygon_clockwise(points, deg_rotation):
    """Rotates a polygon (list of points) around its centroid clockwise by a specified angle.

    Args:
        points (list of array-like): A list of 2D points representing the polygon vertices.
        deg_rotation (float): Rotation angle in degrees.

    Returns:
        list of numpy.ndarray: The rotated polygon points.
    """
    total_x = 0
    total_y = 0
    for point in points:
        total_x = total_x + point[0]
        total_y = total_y + point[0]
    center = np.array([total_x, total_y]) / len(points)
    # Now subtract the center point to get the shape centered about origin
    centered_points = [point - center for point in points]
    centered_points = [
        rotate_point_clockwise(point, deg_rotation) for point in centered_points
    ]
    return [point + center for point in centered_points]


def ballistic_sim(artillery, elevation, target_height):
    """
    Simulates the trajectory of an artillery shell and calculates the final
    position based on initial conditions, gravity, and drag.

    Args:
        artillery (Artillery): The artillery object with mass, drag
        coefficient, and initial velocity.
        elevation (float): Firing angle in degrees.
        target_height (float): The relative height of the target from the
        firing point.

    Returns:
        tuple: The final x-position and time to reach it before the shell hits
        the target or ground.
    """
    delta_t = 0.001
    include_drag = True  # False to just use gravity
    f = artillery.air_drag
    m = artillery.mass
    initial_velocity = artillery.initial_velocity
    t = 0
    position = np.array([0, 0])
    gravity = np.array([0, -9.81])
    velocity = initial_velocity * np.array(
        [math.cos(math.radians(elevation)), math.sin(math.radians(elevation))]
    )
    last_valid_position = position
    while velocity[1] > 0 or position[1] > target_height:
        speed = np.linalg.norm(velocity)
        drag_speed = f * speed * speed / m
        drag_direction = -1 * (velocity / speed)
        drag_vector = drag_speed * drag_direction
        deceleration = drag_vector + gravity if include_drag else gravity

        velocity = velocity + deceleration * delta_t
        last_valid_position = position
        position = position + velocity * delta_t
        t = t + delta_t
    return last_valid_position[0], t - delta_t


def azimuth_to_vert_angle(azimuth):
    """
    Converts an azimuth (horizontal angle) into a vertical angle (clockwise
    from north).

    Args:
        azimuth (float): Azimuth in degrees.

    Returns:
        float: Corresponding vertical angle in degrees.
    """
    return (90 - azimuth) % 360


def azimuth_from_observer_relative(
    mortar_pos: GridCoord,
    observer_pos: GridCoord,
    obs_to_enemy_azimuth: float,
    obs_to_enemy_horiz_distance: float,
):
    """
    Calculates the azimuth and distance from the mortar position to the enemy,
    based on the observer's position and observations.

    Args:
        mortar_pos (GridCoord): Mortar's position in the grid.
        observer_pos (GridCoord): Observer's position in the grid.
        obs_to_enemy_azimuth (float): Azimuth from the observer to the enemy in
        degrees.
        obs_to_enemy_horiz_distance (float): Horizontal distance from the
        observer to the enemy in meters.

    Returns:
        tuple: Azimuth from the mortar to the enemy and the distance in meters.
    """
    enemy_pos = GridCoord(
        observer_pos.easting
        + math.cos(math.radians(azimuth_to_vert_angle(obs_to_enemy_azimuth)))
        * obs_to_enemy_horiz_distance,
        observer_pos.northing
        + math.sin(math.radians(azimuth_to_vert_angle(obs_to_enemy_azimuth)))
        * obs_to_enemy_horiz_distance,
    )

    distance = distancefunc(
        mortar_pos.easting,
        mortar_pos.northing,
        0,
        enemy_pos.easting,
        enemy_pos.northing,
        0,
    )

    return (
        azimuth_from_grids(mortar_pos, enemy_pos),
        distance,
    )


def azimuth_from_grids(start_pos: GridCoord, end_pos: GridCoord):
    """Calculates the azimuth from a starting grid coordinate to an ending grid coordinate.

    Args:
        start_pos (GridCoord): Starting position.
        end_pos (GridCoord): Ending position.

    Returns:
        float: Azimuth from start position to end position (in degrees).
    """
    start_end_vector = GridCoord(
        end_pos.easting - start_pos.easting, end_pos.northing - start_pos.northing
    )

    # since we want azimuth, we need to shift the axes
    # east becomes north, and north becomes west

    temp = start_end_vector.northing
    start_end_vector.northing = start_end_vector.easting
    start_end_vector.easting = temp

    initial = math.degrees(
        math.atan2(start_end_vector.northing, start_end_vector.easting)
    )
    if initial < 0:
        initial = 360 + initial

    return initial


def calculate_elevation(artillery: Artillery, target_height: float, distance: float):
    """
    Determines the optimal firing elevation and time to impact to hit a target
    at a given height and distance.

    Args:
        artillery (Artillery): The artillery object containing mass, drag
        coefficient, and initial velocity.
        target_height (float): Height of the target relative to the artillery.
        distance (float): Horizontal distance to the target in meters.

    Returns:
        dict: Contains 'elevation' in degrees and 'time_to_impact' in seconds.
        str: "Target unreachable" if the target is out of range.
    """
    # Check if target is even reachable using optimal launch angle
    max_attempts = 100
    current_elevation = 45
    current_distance = ballistic_sim(artillery, current_elevation, target_height)[0]
    # Good Ole' Binary Search :)
    if artillery.high_angle:
        max_elevation = 90
        min_elevation = 45
    else:
        max_elevation = 45
        min_elevation = 0
    attempt_count = 0
    while abs(current_distance - distance) > 0.5 and attempt_count < max_attempts:
        attempt_count = attempt_count + 1
        current_elevation = (min_elevation + max_elevation) / 2
        current_distance = ballistic_sim(artillery, current_elevation, target_height)[0]
        if artillery.high_angle:
            if current_distance < distance:
                max_elevation = current_elevation
            else:
                min_elevation = current_elevation
        else:
            if current_distance < distance:
                min_elevation = current_elevation
            else:
                max_elevation = current_elevation
    if abs(current_distance - distance) > 0.5:
        return "Target unreachable."
    return {
        "elevation": round(current_elevation, 1),
        "time_to_impact": round(
            ballistic_sim(artillery, current_elevation, target_height)[1],
            1,
        ),
    }


def generate_distance_elevation_table(artillery, distances):
    """
    Generates a table of elevations required to hit targets at different
    distances and prints the results in miliradianss.

    Args:
        artillery (Artillery): The artillery object containing mass, drag
        coefficient, and initial velocity.
        distances (list): List of distances in meters to generate the elevation
        data for.

    Returns:
        None
    """
    try:
        for distance in distances:
            elevation = calculate_elevation(artillery, 0, distance)["elevation"]
            print(
                f"{distance : >10}",
                "m |",
                f"{round(math.radians(elevation) * 1000, 0) : >5}",
                "milirads",
            )
    except:
        return