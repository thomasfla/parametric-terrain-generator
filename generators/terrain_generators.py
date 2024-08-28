from generators.terrain_flat import generate_flat_terrain
from generators.terrain_perlin import generate_perlin_terrain
from generators.terrain_stairs import generate_pyramid_stairs_terrain
from generators.terrain_blocks import generate_block_terrain
from generators.terrain_slope import generate_slope_terrain
from generators.terrain_checkers import generate_checkers_terrain
from generators.terrain_tilted_squares import generate_tilted_squares_terrain
from generators.terrain_square_centric import generate_square_centric_terrain
import numpy as np
import trimesh
import inspect

def create_border(sizeX, sizeY, borderSize):
    """
    Generate a flat border mesh around a generated terrain.

    Parameters:
    - sizeX (float): Size of the whole terrain along the first axis.
    - sizeY (float): Size of the whole terrain along the second axis.
    - borderSize (float): Size of the border area.

    Returns:
    - trimesh.Trimesh: Mesh object representing the border.
    """
    hX = sizeX * 0.5
    hY = sizeY * 0.5
    center = [hX, hY]
    vertices = np.array(
        [
            [center[0] - hX - borderSize, center[1] - hY - borderSize, 0.0],
            [center[0] + hX + borderSize, center[1] - hY - borderSize, 0.0],
            [center[0] + hX + borderSize, center[1] + hY + borderSize, 0.0],
            [center[0] - hX - borderSize, center[1] + hY + borderSize, 0.0],
            [center[0] - hX, center[1] - hY, 0.0],
            [center[0] + hX, center[1] - hY, 0.0],
            [center[0] + hX, center[1] + hY, 0.0],
            [center[0] - hX, center[1] + hY, 0.0],
        ]
    )
    faces = np.array(
        [
            [0, 1, 5],
            [0, 5, 4],
            [1, 2, 6],
            [1, 6, 5],
            [2, 3, 7],
            [2, 7, 6],
            [3, 0, 4],
            [3, 4, 7],
        ]
    )
    return trimesh.Trimesh(vertices=vertices, faces=faces)


def flat(difficulty, params):
    """
    Generates a 3D terrain mesh that is completely flat.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    mesh = generate_flat_terrain(
        params["terrainSize"],
    )

    return mesh


def stairs_upwards(difficulty, params):
    """
    Generates a 3D terrain mesh with stairs going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_pyramid_stairs_terrain(
        params["terrainSize"],
        params[name]["stepWidth"],
        params[name]["stepHeight"] * difficulty,
        params[name]["platformSize"],
        params[name]["goingUp"],
    )

    return mesh


def stairs_downwards(difficulty, params):
    """
    Generates a 3D terrain mesh with stairs going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_pyramid_stairs_terrain(
        params["terrainSize"],
        params[name]["stepWidth"],
        params[name]["stepHeight"] * difficulty,
        params[name]["platformSize"],
        params[name]["goingUp"],
    )

    return mesh


def slope_upwards(difficulty, params):
    """
    Generates a 3D terrain mesh with a slope going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_slope_terrain(
        params["terrainSize"],
        params[name]["totalHeight"] * difficulty,
        params[name]["barHeight"] * difficulty,
        params[name]["barWidth"],
        params[name]["platformSize"],
        params[name]["goingUp"],
    )

    return mesh


def random_blocks(difficulty, params):
    """
    Generates a 3D terrain mesh using randomly placed blocks.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_block_terrain(
        params["terrainSize"],
        params[name]["minBlockSize"],
        params[name]["maxBlockSize"],
        params[name]["maxBlockHeight"] * difficulty,
        params[name]["platformSize"],
        params[name]["centralPlatform"],
    )

    return mesh


def perlin(difficulty, params):
    """
    Generates a 3D terrain mesh using Perlin noise.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_perlin_terrain(
        params["terrainSize"],
        params[name]["resolutionPerMeter"],
        params[name]["scale"],
        params[name]["heightMultiplier"] * difficulty,
        params[name]["platformSize"],
        params[name]["platformSmoothingDistance"],
        params[name]["edgeSmoothingDistance"],
    )

    return mesh


def checkers(difficulty, params):
    """
    Generates a 3D terrain mesh with a checkers pattern of blocks.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_checkers_terrain(
        params["terrainSize"],
        params[name]["blockSize"],
        params[name]["blockHeight"] * difficulty,
        params[name]["platformSize"],
        params[name]["noise"],
    )

    return mesh


def tilted_squares(difficulty, params):
    """
    Generates a 3D terrain mesh with a filed a square blocks with tilted top.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_tilted_squares_terrain(
        params["terrainSize"],
        params[name]["blockSize"],
        params[name]["blockHeight"] * difficulty,
        params[name]["platformSize"],
        params[name]["noise"] * difficulty,
    )

    return mesh


def square_centric(difficulty, params):
    """
    Generates a 3D terrain mesh with centric square obstacles.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).
    - params (dict): Terrain parameters

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    """

    name = inspect.stack()[0][3]
    mesh = generate_square_centric_terrain(
        params["terrainSize"],
        params[name]["stepWidth"],
        params[name]["stepHeight"] * difficulty,
        params[name]["stepSpacing"],
        params[name]["platformSize"],
    )

    return mesh
