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


def flat(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh that is completely flat.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "flat"
    info["terrain_size"] = terrain_size

    mesh = generate_flat_terrain(
        info["terrain_size"],
    )

    return mesh, info


def stairs_upwards(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh with stairs going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "stairs_upwards"
    info["terrain_size"] = terrain_size
    info["step_width"] = 0.6
    info["step_height"] = 0.08
    info["platform_size"] = 1.0
    info["going_up"] = True

    mesh = generate_pyramid_stairs_terrain(
        info["terrain_size"],
        info["step_width"],
        info["step_height"] * difficulty,
        info["platform_size"],
        info["going_up"],
    )

    return mesh, info


def stairs_downwards(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh with stairs going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "stairs_downwards"
    info["terrain_size"] = terrain_size
    info["step_width"] = 0.6
    info["step_height"] = 0.08
    info["platform_size"] = 1.0
    info["going_up"] = False

    mesh = generate_pyramid_stairs_terrain(
        info["terrain_size"],
        info["step_width"],
        info["step_height"] * difficulty,
        info["platform_size"],
        info["going_up"],
    )

    return mesh, info


def slope_upwards(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh with a slope going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "slope_upwards"
    info["terrain_size"] = terrain_size
    info["total_height"] = 0.5
    info["bar_height"] = 0.08
    info["bar_width"] = 0.2
    info["platform_size"] = 1.0
    info["going_up"] = True

    mesh = generate_slope_terrain(
        info["terrain_size"],
        info["total_height"] * difficulty,
        info["bar_height"] * difficulty,
        info["bar_width"],
        info["platform_size"],
        info["going_up"],
    )

    return mesh, info


def random_blocks(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh using randomly placed blocks.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "random_blocks"
    info["terrain_size"] = terrain_size
    info["min_block_size"] = 0.5
    info["max_block_size"] = 1.0
    info["max_block_height"] = 0.1
    info["platform_size"] = 0.75
    info["central_platform"] = True

    mesh = generate_block_terrain(
        info["terrain_size"],
        info["min_block_size"],
        info["max_block_size"],
        info["max_block_height"] * difficulty,
        info["platform_size"],
        info["central_platform"],
    )

    return mesh, info


def perlin(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh using Perlin noise.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "perlin"
    info["terrain_size"] = terrain_size
    info["resolution_per_meter"] = 20
    info["scale"] = 0.2
    info["height_multiplier"] = 0.3
    info["platform_size"] = 0.75
    info["platform_smoothing_distance"] = 0.4
    info["edge_smoothing_distance"] = 0.4

    mesh = generate_perlin_terrain(
        info["terrain_size"],
        info["resolution_per_meter"],
        info["scale"],
        info["height_multiplier"] * difficulty,
        info["platform_size"],
        info["platform_smoothing_distance"],
        info["edge_smoothing_distance"],
    )

    return mesh, info


def checkers(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh with a checkers pattern of blocks.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "checkers"
    info["terrain_size"] = terrain_size
    info["block_size"] = 0.5
    info["block_height"] = 0.09
    info["platform_size"] = 0.75
    info["noise"] = 0.02

    mesh = generate_checkers_terrain(
        info["terrain_size"],
        info["block_size"],
        info["block_height"] * difficulty,
        info["platform_size"],
        info["noise"],
    )

    return mesh, info


def tilted_squares(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh with a filed a square blocks with tilted top.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "tilted_squares"
    info["terrain_size"] = terrain_size
    info["block_size"] = 0.5
    info["block_height"] = 0.08
    info["platform_size"] = 1.0
    info["noise"] = 0.04

    mesh = generate_tilted_squares_terrain(
        info["terrain_size"],
        info["block_size"],
        info["block_height"] * difficulty,
        info["platform_size"],
        info["noise"] * difficulty,
    )

    return mesh, info


def square_centric(difficulty, terrain_size=8.0):
    """
    Generates a 3D terrain mesh with centric square obstacles.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["name"] = "square_centric"
    info["terrain_size"] = terrain_size
    info["step_width"] = 0.6
    info["step_height"] = 0.08
    info["step_spacing"] = 0.7
    info["platform_size"] = 1.0

    mesh = generate_square_centric_terrain(
        info["terrain_size"],
        info["step_width"],
        info["step_height"] * difficulty,
        info["step_spacing"],
        info["platform_size"],
    )

    return mesh, info
