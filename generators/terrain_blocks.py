import numpy as np
import trimesh
from .utils import create_block, create_square_block, create_square_plane


def create_block_pattern(center, yaw, pattern):
    """
    Generate a pattern of blocks centered at a given point with a given orientation.
    For each number in the pattern, N vertically stacked blocks are placed.
    Stacks are placed next to each other.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - yaw (float): Orientation in yaw.
    - pattern (string): Block pattern like "1", "121", "1221"

    Returns:
    - trimesh.Trimesh: Mesh object representing the pattern.
    """

    # Step parameters
    length = 1.0
    width = 0.3
    block_height = 0.08

    meshes = []
    N = len(pattern)
    y_start = -0.5 * width - width * (N / 2 - 1)
    for i in range(N):
        meshes.append(
            create_block(
                [0.0, y_start + width * i, 0.0],
                length,
                width,
                0.0,
                block_height * int(pattern[i]),
            )
        )
    mesh = trimesh.util.concatenate(meshes)

    # Place the mesh in the world
    rot_matrix = trimesh.transformations.rotation_matrix(yaw, [0, 0, 1], [0.0, 0.0, 0])
    mesh.apply_transform(rot_matrix)
    shift_matrix = np.eye(4)
    shift_matrix[:2, -1] = center[0], center[1]
    mesh.apply_transform(shift_matrix)

    return mesh


def generate_block_terrain(
    terrain_size=8.0,
    min_block_size=0.5,
    max_block_size=1.0,
    max_block_height=0.1,
    platform_size=0.5,
    central_platform=True,
):
    """
    Generate a mesh for a pyramid stairs terrain.

    Parameters:
    - terrain_size (float): Size of the terrain.
    - min_block_size (float): Minimum size of each block.
    - max_block_size (float): Maximum size of each block.
    - max_block_height (float): Maximum height of each block.
    - platform_size (float): Size of the central platform.
    - central_platform (bool): True to place a central platform.

    Returns:
    - trimesh.Trimesh: Mesh object representing the pyramid stairs terrain.
    """

    meshes = []

    # Terrain flat square
    meshes.append(
        create_square_plane([terrain_size / 2.0, terrain_size / 2.0], terrain_size, 0.0)
    )

    # Add blocks of various heights
    N = 100
    outer_margin = max_block_size * 0.75
    inner_margin = max_block_size * 0.75 + platform_size * 0.5
    k = 0
    while k < N:
        xy = np.random.random(2) * (terrain_size - 2 * outer_margin) + outer_margin
        if np.all(np.abs(xy - terrain_size / 2) < inner_margin):
            # Resample if too close from central platform
            continue

        # Step parameters
        yaw = np.random.random() * 3.1415
        length = np.random.random() * (max_block_size - min_block_size) + min_block_size
        width = np.random.random() * (max_block_size - min_block_size) + min_block_size
        block_height = np.random.random() * max_block_height

        meshes.append(create_block(xy, length, width, 0.0, block_height, yaw))
        k += 1

    # Central platform
    if central_platform:
        meshes.append(
            create_square_block(
                [terrain_size / 2, terrain_size / 2],
                platform_size,
                0.0,
                0.5 * max_block_height,
            )
        )

    return trimesh.util.concatenate(meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_block_terrain()

    # Display mesh with colormap along the Z axis
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="viridis"
    )
    trimesh.Scene(mesh).show()

    # Export mesh as .obj file
    # mesh.export(file_obj='terrain.obj', file_type='obj')
