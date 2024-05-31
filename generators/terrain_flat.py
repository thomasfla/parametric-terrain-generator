import numpy as np
import trimesh
from .utils import (
    create_square_plane,
)


def generate_flat_terrain(terrain_size=8.0):
    """
    Generate a mesh for a flat terrain.

    Parameters:
    - terrain_size (float): Size of the terrain.

    Returns:
    - trimesh.Trimesh: Mesh object representing the flat terrain.
    """
    center = [terrain_size / 2.0, terrain_size / 2.0]
    meshes = []

    # Flat plane
    meshes.append(create_square_plane(center, terrain_size, 0.0))

    return trimesh.util.concatenate(meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_flat_terrain()

    # Display mesh
    trimesh.Scene(mesh).show()

    # Export mesh as .obj file
    # mesh.export(file_obj='terrain.obj', file_type='obj')
