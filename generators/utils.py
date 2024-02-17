import numpy as np
import trimesh


def create_plane(center, length, width, z_height, yaw=0):
    """
    Generate a plane mesh centered at a given point.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the square plane.
    - length (float): Size of the block along the first axis.
    - width (float): Size of the block along the second axis.
    - z_height (float): Z-coordinate (height) of the plane.
    - yaw (float): Orientation in yaw.

    Returns:
    - trimesh.Trimesh: Mesh object representing the square plane.
    """
    half_length = length / 2
    half_width = width / 2
    corners = np.array(
        [
            [center[0] - half_length, center[1] - half_width, z_height],
            [center[0] + half_length, center[1] - half_width, z_height],
            [center[0] + half_length, center[1] + half_width, z_height],
            [center[0] - half_length, center[1] + half_width, z_height],
        ]
    )
    faces = np.array([[0, 1, 2], [0, 2, 3]])

    mesh = trimesh.Trimesh(vertices=corners, faces=faces)
    if yaw != 0:
        rot_matrix = trimesh.transformations.rotation_matrix(
            yaw, [0, 0, 1], [center[0], center[1], 0]
        )
        mesh.apply_transform(rot_matrix)

    return mesh


def create_square_plane(center, width, z_height, yaw=0):
    """
    Generate a plane mesh centered at a given point.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the square plane.
    - width (float): Width of the square plane.
    - z_height (float): Z-coordinate (height) of the plane.
    - yaw (float): Orientation in yaw.

    Returns:
    - trimesh.Trimesh: Mesh object representing the square plane.
    """
    return create_plane(center, width, width, z_height, yaw)


def create_wall(center, length, width, height, step_height, yaw=0):
    """
    Generate a wall mesh with a specified base center, size, and height.

    Parameters:
    - center (tuple/list of float): Center of the base of the wall.
    - length (float): Size of the wall along the first axis.
    - width (float): Size of the wall along the second axis.
    - height (float): Base height of the wall.
    - step_height (float): Additional height for the top vertices of the wall.
    - yaw (float): Orientation in yaw.

    Returns:
    - trimesh.Trimesh: Mesh object representing the wall.
    """
    half_length = length / 2
    half_width = width / 2
    base_z = height
    top_z = height + step_height
    vertices = np.array(
        [
            [center[0] - half_length, center[1] - half_width, base_z],
            [center[0] + half_length, center[1] - half_width, base_z],
            [center[0] + half_length, center[1] + half_width, base_z],
            [center[0] - half_length, center[1] + half_width, base_z],
            [center[0] - half_length, center[1] - half_width, top_z],
            [center[0] + half_length, center[1] - half_width, top_z],
            [center[0] + half_length, center[1] + half_width, top_z],
            [center[0] - half_length, center[1] + half_width, top_z],
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

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    if yaw != 0:
        rot_matrix = trimesh.transformations.rotation_matrix(
            yaw, [0, 0, 1], [center[0], center[1], 0]
        )
        mesh.apply_transform(rot_matrix)

    return mesh


def create_square_wall(center, width, height, step_height, yaw=0):
    """
    Generate a squared wall mesh with a specified base center, size, and height.

    Parameters:
    - center (tuple/list of float): Center of the base of the wall.
    - width (float): Width of the sides of the wall.
    - height (float): Base height of the wall.
    - step_height (float): Additional height for the top vertices of the wall.
    - yaw (float): Orientation in yaw.

    Returns:
    - trimesh.Trimesh: Mesh object representing the wall.
    """
    return create_wall(center, width, width, height, step_height, yaw)


def create_block(center, length=1.0, width=0.3, height=0.0, block_height=0.08, yaw=0):
    """
    Generate a block mesh centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - length (float): Size of the block along the first axis.
    - width (float): Size of the block along the second axis.
    - height (float): Base height of the block.
    - block_height (float): Additional height for the top vertices of the block.
    - yaw (float): Orientation in yaw.

    Returns:
    - trimesh.Trimesh: Mesh object representing the block.
    """

    mesh_top = create_plane(center, length, width, height + block_height)
    mesh_side = create_wall(center, length, width, height, block_height)
    mesh = trimesh.util.concatenate([mesh_top, mesh_side])
    if yaw != 0:
        rot_matrix = trimesh.transformations.rotation_matrix(
            yaw, [0, 0, 1], [center[0], center[1], 0]
        )
        mesh.apply_transform(rot_matrix)

    return mesh


def create_square_block(center, width=0.3, height=0.0, block_height=0.08, yaw=0):
    """
    Generate a square block mesh centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - width (float): Width of the block.
    - height (float): Base height of the block.
    - block_height (float): Additional height for the top vertices of the block.
    - yaw (float): Orientation in yaw.

    Returns:
    - trimesh.Trimesh: Mesh object representing the block.
    """
    return create_block(center, width, width, height, block_height, yaw)


def create_block_tilted_top(
    center, length=1.0, width=0.3, height=0.0, block_height=0.08, yaw=0, noise=0.02
):
    """
    Generate a block mesh centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - length (float): Size of the block along the first axis.
    - width (float): Size of the block along the second axis.
    - height (float): Base height of the block.
    - block_height (float): Additional height for the top vertices of the block.
    - yaw (float): Orientation in yaw.
    - noise (float): Noise to disturb the top surface with.

    Returns:
    - trimesh.Trimesh: Mesh object representing the block.
    """

    mesh_top = create_plane(center, length, width, height + block_height)
    mesh_side = create_wall(center, length, width, height, block_height)
    mesh = trimesh.util.concatenate([mesh_top, mesh_side])

    # Moving up and down the vertices of the top of the block to create the tilting
    A = mesh.vertices[:, 2] == height + block_height  # Selecting the top vertices
    B = mesh.vertices[:, 0] == (
        center[0] + length / 2
    )  # Selecting the vertices on positive X
    C = mesh.vertices[:, 1] == (
        center[1] + width / 2
    )  # Selecting the vertices on positive Y
    nXY = (2 * np.random.random(2) - 1) * noise  # Tilting magnitude along X and Y
    mesh.vertices[A * B, 2] += nXY[0]
    mesh.vertices[A * ~B, 2] -= nXY[0]
    mesh.vertices[A * C, 2] += nXY[1]
    mesh.vertices[A * ~C, 2] -= nXY[1]

    if yaw != 0:
        rot_matrix = trimesh.transformations.rotation_matrix(
            yaw, [0, 0, 1], [center[0], center[1], 0]
        )
        mesh.apply_transform(rot_matrix)

    return mesh


def create_square_plane_with_hole(center, outer_size, inner_size, height):
    """
    Generate a square plane with a square hole.

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
