import numpy as np
import trimesh


def create_square_plane(center, width, z_height):
    """
    Generate a square plane mesh centered at a given point.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the square plane.
    - width (float): Width of the square plane.
    - z_height (float): Z-coordinate (height) of the plane.

    Returns:
    - trimesh.Trimesh: Mesh object representing the square plane.
    """
    half_width = width / 2
    corners = np.array(
        [
            [center[0] - half_width, center[1] - half_width, z_height],
            [center[0] + half_width, center[1] - half_width, z_height],
            [center[0] + half_width, center[1] + half_width, z_height],
            [center[0] - half_width, center[1] + half_width, z_height],
        ]
    )
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    return trimesh.Trimesh(vertices=corners, faces=faces)


def create_wall(center, size, height, step_height):
    """
    Generate a squared wall mesh with a specified base center, size, and height.

    Parameters:
    - center (tuple/list of float): Center of the base of the wall.
    - size (float): Length and width of the wall base.
    - height (float): Base height of the wall.
    - step_height (float): Additional height for the top vertices of the wall.

    Returns:
    - trimesh.Trimesh: Mesh object representing the wall.
    """
    half_size = size / 2
    base_z = height
    top_z = height + step_height
    vertices = np.array(
        [
            [center[0] - half_size, center[1] - half_size, base_z],
            [center[0] + half_size, center[1] - half_size, base_z],
            [center[0] + half_size, center[1] + half_size, base_z],
            [center[0] - half_size, center[1] + half_size, base_z],
            [center[0] - half_size, center[1] - half_size, top_z],
            [center[0] + half_size, center[1] - half_size, top_z],
            [center[0] + half_size, center[1] + half_size, top_z],
            [center[0] - half_size, center[1] + half_size, top_z],
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


def create_step_top(center, outer_size, inner_size, height):
    """
    Generate a step top mesh, a square plane with a square hole.

    Parameters:
    - center (tuple/list of float): Center of the square.
    - outer_size (float): Size of the outer square.
    - inner_size (float): Size of the inner square (hole).
    - height (float): Z-coordinate (height) of the plane.

    Returns:
    - trimesh.Trimesh: Mesh object representing the step top.
    """
    half_outer = outer_size / 2
    half_inner = inner_size / 2
    vertices = np.array(
        [
            [center[0] - half_outer, center[1] - half_outer, height],
            [center[0] + half_outer, center[1] - half_outer, height],
            [center[0] + half_outer, center[1] + half_outer, height],
            [center[0] - half_outer, center[1] + half_outer, height],
            [center[0] - half_inner, center[1] - half_inner, height],
            [center[0] + half_inner, center[1] - half_inner, height],
            [center[0] + half_inner, center[1] + half_inner, height],
            [center[0] - half_inner, center[1] + half_inner, height],
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


def generate_pyramid_stairs_terrain(
    terrain_size=8.0, step_width=0.2, step_height=0.05, platform_size=0.5, going_up=True
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
        step_mesh = create_step_top(center, outer_size, inner_size, height)
        wall_mesh = create_wall(center, inner_size, height, -sign * step_height)
        meshes.append(step_mesh)
        meshes.append(wall_mesh)

    return trimesh.util.concatenate(meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_pyramid_stairs_terrain()
    scene = mesh.show()
    # mesh.export(file_obj='terrain.obj', file_type='obj')
    from IPython import embed

    embed()
