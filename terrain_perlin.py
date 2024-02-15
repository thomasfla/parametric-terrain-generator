import numpy as np
import trimesh
from noise import pnoise2


def generate_perlin_terrain(
    terrain_size=8.0,
    resolution_per_meter=20,
    scale=0.2,
    height_multiplier=0.3,
    platform_size=0.5,
    platform_smoothing_distance=0.4,
    edge_smoothing_distance=0.4,
):
    """
    Generates a 3D terrain mesh using Perlin noise, with an optional flat platform in the center and smoothed edges.

    Parameters:
    - terrain_size (float): The size of the square terrain side in meters.
    - resolution_per_meter (int): The number of vertices to generate per meter.
    - scale (float): The scale of the Perlin noise, influencing the frequency of terrain features.
    - height_multiplier (float): Multiplier for the terrain height, adjusting the vertical scale of features.
    - platform_size (float): The size of the square platform in the center of the terrain, in meters.
    - platform_smoothing_distance (float): The distance over which the edges of the central platform are smoothed, in meters.
    - edge_smoothing_distance (float): The distance over which the terrain edges are smoothed, in meters.

    Returns:
    - A trimesh.Trimesh object representing the generated terrain mesh. This mesh includes vertices for the terrain's surface and faces that define the 3D shape.
    """
    terrain_resolution = int(terrain_size * resolution_per_meter)  # Total resolution

    # Platform parameters
    # platform_size = 0.5  # Platform size in meters
    platform_resolution = int(
        platform_size * resolution_per_meter
    )  # Platform resolution in vertices
    platform_height = 0.0  # Height of the platform in meters
    platform_center = terrain_resolution // 2  # Center the platform

    # Smoothing parameters
    platform_smoothness = (
        platform_smoothing_distance * resolution_per_meter
    )  # Number of vertices over which to smooth the platform edges
    edge_smoothness = (
        edge_smoothing_distance * resolution_per_meter
    )  # Number of vertices over which to smooth the terrain edges

    # Generate the heightmap
    # Random shift (xs, ys) to avoid always generating the same map
    xs, ys = 1000 * np.random.random(2)
    heightmap = np.zeros((terrain_resolution + 1, terrain_resolution + 1))
    for x in range(terrain_resolution):
        for y in range(terrain_resolution):
            # Calculate normalized coordinates
            nx = (x + xs) / terrain_resolution
            ny = (y + ys) / terrain_resolution

            # Generate base height using Perlin noise
            base_height = pnoise2(nx / scale, ny / scale, octaves=4) * height_multiplier

            # Calculate distance to the nearest edge for edge smoothing
            edge_dist = min(
                x, y, terrain_resolution - x - 1, terrain_resolution - y - 1
            )
            edge_factor = min(1, edge_dist / edge_smoothness)

            # Calculate distance to the center of the platform
            dist_to_center = max(abs(x - platform_center), abs(y - platform_center))
            # Calculate smoothing factor for the platform edge
            if dist_to_center < platform_resolution / 2 + platform_smoothness:
                platform_edge_dist = max(0, dist_to_center - platform_resolution / 2)
                smooth_factor = max(0, 1 - platform_edge_dist / platform_smoothness)
                height = (platform_height * smooth_factor) + (
                    base_height * (1 - smooth_factor)
                )
            else:
                height = base_height

            # Apply edge smoothing
            height *= edge_factor

            heightmap[x, y] = height

    # Convert heightmap to mesh
    vertices = []
    faces = []
    for x in range(terrain_resolution):
        for y in range(terrain_resolution):
            v0 = [x / resolution_per_meter, y / resolution_per_meter, heightmap[x, y]]
            v1 = [
                (x + 1) / resolution_per_meter,
                y / resolution_per_meter,
                heightmap[x + 1, y],
            ]
            v2 = [
                x / resolution_per_meter,
                (y + 1) / resolution_per_meter,
                heightmap[x, y + 1],
            ]
            v3 = [
                (x + 1) / resolution_per_meter,
                (y + 1) / resolution_per_meter,
                heightmap[x + 1, y + 1],
            ]

            idx_base = len(vertices)
            vertices.extend([v0, v1, v2, v3])
            faces.append([idx_base, idx_base + 1, idx_base + 2])
            faces.append([idx_base + 2, idx_base + 1, idx_base + 3])
    return trimesh.Trimesh(vertices=vertices, faces=faces)


if __name__ == "__main__":
    # Usage:
    mesh = generate_perlin_terrain()

    # Display mesh with colormap along the Z axis
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="viridis"
    )
    trimesh.Scene(mesh).show()

    # Export mesh to .obj file
    # mesh.export("terrain.obj")
