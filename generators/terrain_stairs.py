import numpy as np
import trimesh
from .utils import (
    create_square_plane,
    create_square_wall,
    create_square_plane_with_hole,
)


def generate_pyramid_stairs_terrain(
    terrain_size=8.0, step_width=0.6, step_height=0.08, platform_size=1.0, going_up=True
):
    """
    Generate a mesh for a pyramid stairs terrain.

    Parameters:
    - terrain_size (float): Size of the terrain.
    - step_width (float): Width of each step.
    - step_height (float): Height of each step.
    - platform_size (float): Size of the central platform.
    - going_up (bool): Direction of the stairs, True for going up.

    Returns:
    - trimesh.Trimesh: Mesh object representing the pyramid stairs terrain.
    """
    center = [terrain_size / 2.0, terrain_size / 2.0]
    num_steps = int(((terrain_size - platform_size) / 2.0) / step_width)
    total_height = num_steps * step_height
    sign = 1 if going_up else -1
    meshes = []

    # Central platform
    meshes.append(create_square_plane(center, platform_size, -sign * total_height))

    for i in range(num_steps):
        outer_size = platform_size + 2 * step_width * (i + 1)
        outer_size = terrain_size if i == num_steps - 1 else outer_size
        inner_size = platform_size + 2 * step_width * i
        height = sign * (step_height * (i + 1) - total_height)
        step_mesh = create_square_plane_with_hole(
            center, outer_size, inner_size, height
        )
        wall_mesh = create_square_wall(center, inner_size, height, -sign * step_height)
        meshes.append(step_mesh)
        meshes.append(wall_mesh)

    return trimesh.util.concatenate(meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_pyramid_stairs_terrain()

    # Display mesh with colormap along the Z axis
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="viridis"
    )
    trimesh.Scene(mesh).show()

    # Export mesh as .obj file
    # mesh.export(file_obj='terrain.obj', file_type='obj')
