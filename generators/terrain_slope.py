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


def create_bar(center, alpha, outer_size, inner_size, bar_height, bar_width):
    """
    Generate a block mesh centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - alpha (float): Relative position on the slope between 0 and 1.
    - outer_size (float): Size of the outer square.
    - inner_size (float): Size of the inner square (hole).
    - bar_height (float): Width of the transversal bars on the slope.
    - bar_width (float): Height of the transversal bars on the slope.

    Returns:
    - trimesh.Trimesh: Mesh object representing the bar.
    """
    half_outer = outer_size / 2
    half_inner = inner_size / 2
    dxy = alpha * (half_outer - half_inner)
    bw = bar_width / 2

    corners = np.array(
        [
            [center[0] + half_inner + dxy - bw, center[1] + half_inner + dxy - bw, 0.0],
            [center[0] + half_inner + dxy - bw, center[1] - half_inner - dxy + bw, 0.0],
            [
                center[0] + half_inner + dxy - bw,
                center[1] + half_inner + dxy - bw,
                bar_height,
            ],
            [
                center[0] + half_inner + dxy - bw,
                center[1] - half_inner - dxy + bw,
                bar_height,
            ],
            [center[0] + half_inner + dxy + bw, center[1] + half_inner + dxy + bw, 0.0],
            [center[0] + half_inner + dxy + bw, center[1] - half_inner - dxy - bw, 0.0],
            [
                center[0] + half_inner + dxy + bw,
                center[1] + half_inner + dxy + bw,
                bar_height,
            ],
            [
                center[0] + half_inner + dxy + bw,
                center[1] - half_inner - dxy - bw,
                bar_height,
            ],
        ]
    )
    faces = np.array(
        [
            [0, 1, 2],
            [1, 3, 2],
            [4, 6, 5],
            [5, 6, 7],
            [1, 5, 7],
            [1, 7, 3],
            [4, 0, 2],
            [4, 2, 6],
            [3, 7, 6],
            [3, 6, 2],
        ]
    )
    mesh = trimesh.Trimesh(vertices=corners, faces=faces)

    return mesh


def generate_smooth_slope_side(center, yaw, outer_size, inner_size, height):
    """
    Generate a smooth slope centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - yaw (float): Orientation in yaw.
    - outer_size (float): Size of the outer square.
    - inner_size (float): Size of the inner square (hole).
    - height (float): Z-coordinate (height) of the plane.

    Returns:
    - trimesh.Trimesh: Mesh object representing the slope.
    """
    half_outer = outer_size / 2
    half_inner = inner_size / 2
    vertices = np.array(
        [
            [center[0] + half_outer, center[1] - half_outer, 0.0],
            [center[0] + half_outer, center[1] + half_outer, 0.0],
            [center[0] + half_inner, center[1] + half_inner, height],
            [center[0] + half_inner, center[1] - half_inner, height],
        ]
    )
    faces = np.array(
        [
            [0, 1, 2],
            [2, 3, 0],
        ]
    )

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Place the mesh in the world
    rot_matrix = trimesh.transformations.rotation_matrix(
        yaw, [0, 0, 1], [center[0], center[1], 0]
    )
    mesh.apply_transform(rot_matrix)

    return mesh


def generate_barred_slope_side(
    center, yaw, outer_size, inner_size, height, bar_height, bar_width
):
    """
    Generate a slope with bars centered at a given point with a given orientation.

    Parameters:
    - center (tuple/list of float): Center point (x, y) of the block.
    - yaw (float): Orientation in yaw.
    - outer_size (float): Size of the outer square.
    - inner_size (float): Size of the inner square (hole).
    - bar_height (float): Width of the transversal bars on the slope.
    - bar_width (float): Height of the transversal bars on the slope.

    Returns:
    - trimesh.Trimesh: Mesh object representing the slope.
    """
    half_outer = outer_size / 2
    half_inner = inner_size / 2
    vertices = np.array(
        [
            [center[0] + half_outer, center[1] - half_outer, 0.0],
            [center[0] + half_outer, center[1] + half_outer, 0.0],
            [center[0] + half_inner, center[1] + half_inner, 0.0],
            [center[0] + half_inner, center[1] - half_inner, 0.0],
        ]
    )
    faces = np.array(
        [
            [0, 1, 2],
            [2, 3, 0],
        ]
    )

    slope_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Create transversal bars on the smooth slope
    bars_mesh = trimesh.util.concatenate(
        [
            create_bar(center, a, outer_size, inner_size, bar_height, bar_width)
            for a in [0.25, 0.5, 0.75]
        ]
    )
    rot = np.arctan2(height, half_outer - half_inner)
    rot_matrix = trimesh.transformations.rotation_matrix(
        rot, [0, 1, 0], [center[0] + half_inner, center[1], 0]
    )
    slope_mesh.apply_transform(rot_matrix)
    bars_mesh.apply_transform(rot_matrix)
    shift_matrix = np.eye(4)
    shift_matrix[2, -1] = height
    slope_mesh.apply_transform(shift_matrix)
    bars_mesh.apply_transform(shift_matrix)

    # Merge slope and bars
    mesh = trimesh.util.concatenate([slope_mesh, bars_mesh])

    # Correction along X
    maxx = np.max(slope_mesh.vertices[:, 0] - center[0] - half_inner)
    coeff = (half_outer - half_inner) / maxx
    mesh.vertices[:, 0] = (
        coeff * (mesh.vertices[:, 0] - center[0] - half_inner) + center[0] + half_inner
    )

    # Correction along Z
    if height < 0:
        minmaxz = np.max(slope_mesh.vertices[:, 2] - height)
    else:
        minmaxz = np.min(slope_mesh.vertices[:, 2] - height)
    coeff = -height / minmaxz
    mesh.vertices[:, 2] = coeff * (mesh.vertices[:, 2] - height) + height

    # Place the mesh in the world
    rot_matrix = trimesh.transformations.rotation_matrix(
        yaw, [0, 0, 1], [center[0], center[1], 0]
    )
    mesh.apply_transform(rot_matrix)

    return mesh


def generate_slope_terrain(
    terrain_size=8.0,
    total_height=1.0,
    bar_height=0.2,
    bar_width=0.2,
    platform_size=1.0,
    going_up=True,
):
    """
    Generate a mesh for a sloped terrain.

    Parameters:
    - terrain_size (float): Size of the terrain.
    - total_height (float): Total height of the slope.
    - bar_height (float): Width of the transversal bars on the slope.
    - bar_width (float): Height of the transversal bars on the slope.
    - platform_size (float): Size of the central platform.
    - going_up (bool): Direction of the slope, True for going up.

    Returns:
    - trimesh.Trimesh: Mesh object representing the pyramid stairs terrain.
    """
    center = [terrain_size / 2.0, terrain_size / 2.0]
    sign = 1 if going_up else -1
    meshes = []

    # Flat terrain
    if total_height == 0.0:
        return create_square_plane(center, terrain_size, 0.0)

    # Central platform
    meshes.append(create_square_plane(center, platform_size, -sign * total_height))

    # North slope
    slope_mesh = generate_smooth_slope_side(
        center, 0.0, terrain_size - 2.0, platform_size, -sign * total_height
    )
    meshes.append(slope_mesh)

    # West slope
    barred_slope_mesh = generate_barred_slope_side(
        center,
        np.pi / 2,
        terrain_size - 2.0,
        platform_size,
        -sign * total_height,
        bar_height,
        bar_width,
    )
    meshes.append(barred_slope_mesh)

    # South slope
    slope_mesh = generate_smooth_slope_side(
        center, np.pi, terrain_size - 2.0, platform_size, -sign * total_height
    )
    meshes.append(slope_mesh)

    # East slope
    barred_slope_mesh = generate_barred_slope_side(
        center,
        3 * np.pi / 2,
        terrain_size - 2.0,
        platform_size,
        -sign * total_height,
        bar_height,
        bar_width,
    )
    meshes.append(barred_slope_mesh)

    step_mesh = create_step_top(center, terrain_size, terrain_size - 2.0, 0.0)
    meshes.append(step_mesh)

    return trimesh.util.concatenate(meshes)


if __name__ == "__main__":
    # Usage:
    mesh = generate_slope_terrain()

    # Display mesh with colormap along the Z axis
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="viridis"
    )
    trimesh.Scene(mesh).show()

    # Export mesh as .obj file
    # mesh.export(file_obj='terrain.obj', file_type='obj')
