import numpy as np
import trimesh
from .utils import (
    create_square_plane,
    create_square_wall,
    create_square_plane_with_hole,
)


def create_square_obstacle(center, outer_size, inner_size, height, step_height):
    mesh_inner = create_square_wall(
        center, inner_size, height + step_height, -step_height
    )
    mesh_outer = create_square_wall(center, outer_size, height, step_height)
    mesh_top = create_square_plane_with_hole(
        center, outer_size, inner_size, height + step_height
    )

    return trimesh.util.concatenate([mesh_inner, mesh_top, mesh_outer])


def generate_square_centric_terrain(
    terrain_size=8.0,
    step_width=0.3,
    step_height=0.08,
    step_spacing=0.7,
    platform_size=1.0,
):
    """
    Generate a mesh with square obstacles centered on the central platform.

    Parameters:
    - terrain_size (float): Size of the terrain.
    - step_width (float): Width of each step.
    - step_height (float): Height of each step.
    - step_spacing (float): Spacing between the steps.
    - platform_size (float): Size of the central platform.

    Returns:
    - trimesh.Trimesh: Mesh object representing the square centric terrain.
    """
    center = [terrain_size / 2.0, terrain_size / 2.0]
    num_steps = int(((terrain_size - platform_size) / 2.0) / step_spacing)

    meshes = []

    # Central platform
    meshes.append(create_square_plane(center, terrain_size, 0.0))

    # Square obstacles
    for i in range(num_steps):
        inner_size = platform_size + 2 * step_spacing * i
        outer_size = inner_size + step_width
        meshes.append(
            create_square_obstacle(center, outer_size, inner_size, 0.0, step_height)
        )

    return trimesh.util.concatenate(meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_square_centric_terrain()

    # Display mesh with colormap along the Z axis
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="viridis"
    )
    trimesh.Scene(mesh).show()

    # Export mesh as .obj file
    # mesh.export(file_obj='terrain.obj', file_type='obj')
