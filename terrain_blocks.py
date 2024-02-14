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


def create_block(center, yaw, length=1.0, width=0.3, block_height=0.08):
    """
    Generate a block mesh centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - yaw (float): Orientation in yaw.
    - length (float): Size of the block along the first axis.
    - width (float): Size of the block along the second axis.
    - block_height (float): Height of the block.

    Returns:
    - trimesh.Trimesh: Mesh object representing the block.
    """
    half_length = length / 2
    half_width = width / 2
    corners = np.array(
        [
            [center[0] - half_length, center[1] - half_width, block_height],
            [center[0] + half_length, center[1] - half_width, block_height],
            [center[0] + half_length, center[1] + half_width, block_height],
            [center[0] - half_length, center[1] + half_width, block_height],
            [center[0] - half_length, center[1] - half_width, 0.0],
            [center[0] + half_length, center[1] - half_width, 0.0],
            [center[0] + half_length, center[1] + half_width, 0.0],
            [center[0] - half_length, center[1] + half_width, 0.0],
        ]
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [0, 4, 1],
            [4, 5, 1],
            [1, 5, 2],
            [5, 6, 2],
            [2, 6, 3],
            [6, 7, 3],
            [3, 7, 0],
            [7, 4, 0],
        ]
    )
    mesh = trimesh.Trimesh(vertices=corners, faces=faces)

    # Rotate the mesh along the Z axis
    if yaw != 0.0:
        direction = [0, 0, 1]
        center += [0.0]
        rot_matrix = trimesh.transformations.rotation_matrix(yaw, direction, center)
        mesh.apply_transform(rot_matrix)

    return mesh


def create_block_pattern(center, yaw, pattern):
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
                0.0,
                length,
                width,
                block_height * int(pattern[i]),
            )
        )
    mesh = trimesh.util.concatenate(meshes)

    # Place the mesh in the world
    rot_matrix = trimesh.transformations.rotation_matrix(yaw, [0, 0, 1], [0, 0, 0])
    rot_matrix[:2, -1] = center[0], center[1]
    mesh.apply_transform(rot_matrix)

    return mesh


def create_block(center, yaw, length, width, block_height):
    mesh = create_block(
        [0.0, 0.0],
        0.0,
        length,
        width,
        block_height,
    )

    # Place the mesh in the world
    rot_matrix = trimesh.transformations.rotation_matrix(yaw, [0, 0, 1], [0, 0, 0])
    rot_matrix[:2, -1] = center[0], center[1]
    mesh.apply_transform(rot_matrix)

    return mesh


def generate_block_terrain(
    terrain_size=8.0,
    block_width=0.6,
    block_height=0.08,
    platform_size=1.0,
    going_up=True,
):
    """
    Generate a mesh for a pyramid stairs terrain.

    Parameters:
    - terrain_size (float): Size of the terrain.
    - block_width (float): Width of each block.
    - block_height (float): Height of each block.
    - platform_size (float): Size of the central platform.
    - going_up (bool): Direction of the stairs, True for going up.

    Returns:
    - trimesh.Trimesh: Mesh object representing the pyramid stairs terrain.
    """
    center = [terrain_size / 2.0, terrain_size / 2.0]
    num_blocks = int(((terrain_size - platform_size) / 2.0) / block_width)
    total_height = num_blocks * block_height
    sign = 1 if going_up else -1
    meshes = []

    # Central platform
    meshes.append(create_square_plane(center, terrain_size, 0.0))

    # meshes.append(create_block([3.0, 4.0], 0.0, 1.0, 0.3, 0.08))
    # meshes.append(create_block([5.0, 4.0], np.pi/4 , 1.0, 0.3, 0.16))

    N = 100
    xy = np.random.random((N, 2)) * 6.5 - 3.25
    nXY = np.linalg.norm(xy, axis=1)
    nLim = 1.2
    xy[nXY < nLim] = xy[nXY < nLim] / nXY[nXY < nLim].reshape((-1, 1)) * nLim
    xy += np.array([4.0, 4.0])
    for k in range(N):
        # Step parameters
        yaw = np.random.random() * 3.1415
        length = 0.5 + np.random.random() * 0.5
        width = 0.5 + np.random.random() * 0.5
        block_height = np.random.random() * 0.10

        meshes.append(create_block(xy[k], yaw, length, width, block_height))

    meshes.append(create_block([4.0, 4.0], 0.0, 0.5, 0.5, 0.2))

    """for i in range(num_blocks):
        outer_size = platform_size + 2 * block_width * (i + 1)
        outer_size = terrain_size if i == num_blocks - 1 else outer_size
        inner_size = platform_size + 2 * block_width * i
        height = sign * (block_height * (i + 1) - total_height)
        block_mesh = create_block_top(center, outer_size, inner_size, height)
        wall_mesh = create_wall(center, inner_size, height, -sign * block_height)
        meshes.append(block_mesh)
        meshes.append(wall_mesh)"""

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
