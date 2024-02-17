import numpy as np
import trimesh
from .utils import (
    create_square_plane,
    create_square_plane_with_hole,
    create_block_tilted_top,
)


def generate_tilted_squares_terrain(
    terrain_size=8.0,
    block_size=0.5,
    block_height=0.08,
    platform_size=1.0,
    noise=0.04,
):
    """
    Generate a mesh for a pyramid stairs terrain.

    Parameters:
    - terrain_size (float): Size of the terrain.
    - block_size (float): Size of the checker blocks.
    - block_height (float): Height of the checker blocks.
    - platform_size (float): Size of the central platform.
    - noise (float): Random noise applied to the block heights.

    Returns:
    - trimesh.Trimesh: Mesh object representing the checkers terrain.
    """

    N = int(terrain_size / block_size)
    center = [terrain_size / 2, terrain_size / 2]

    # Flat border area around the checkers
    border_mesh = create_square_plane_with_hole(
        center, terrain_size, terrain_size - 2 * block_size, 0.0
    )

    tilted_meshes = []
    for i in range(1, N - 1):
        x = (i + 0.5) * block_size
        for j in range(1, N - 1):
            y = (j + 0.5) * block_size
            if np.all(np.abs(np.array([x, y]) - np.array(center)) < platform_size / 2):
                tilted_meshes.append(create_square_plane([x, y], block_size, 0.0))

            else:
                tilted_meshes.append(
                    create_block_tilted_top(
                        [x, y], block_size, block_size, 0.0, block_height, 0.0, noise
                    )
                )

    tilted_meshes.append(border_mesh)
    return trimesh.util.concatenate(tilted_meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_tilted_squares_terrain()

    # Display mesh with colormap along the Z axis
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="viridis"
    )
    trimesh.Scene(mesh).show()

    # Export mesh as .obj file
    # mesh.export(file_obj='terrain.obj', file_type='obj')
