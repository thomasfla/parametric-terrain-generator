from terrain_perlin import generate_perlin_terrain
from terrain_stairs import generate_pyramid_stairs_terrain
from terrain_blocks import generate_block_terrain


def stairs_upwards(difficulty):
    """
    Generates a 3D terrain mesh with stairs going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["terrain_size"] = 8.0
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


def stairs_downwards(difficulty):
    """
    Generates a 3D terrain mesh with stairs going upwards.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["terrain_size"] = 8.0
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


def blocks(difficulty):
    """
    Generates a 3D terrain mesh using randomly placed blocks.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["terrain_size"] = 8.0
    info["min_block_size"] = 0.5
    info["max_block_size"] = 1.0
    info["max_block_height"] = 0.1
    info["platform_size"] = 0.5
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


def perlin(difficulty):
    """
    Generates a 3D terrain mesh using Perlin noise.

    Parameters:
    - difficulty (float): Difficulty scaling between 0 (easiest) and 1 (hardest).

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh.
    - A dict containing the parameters of the terrain generator.
    """

    info = {}
    info["terrain_size"] = 8.0
    info["resolution_per_meter"] = 20
    info["scale"] = 0.2
    info["height_multiplier"] = 0.3
    info["platform_size"] = 0.5
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
