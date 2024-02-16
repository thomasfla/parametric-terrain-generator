import matplotlib.pyplot as plt
import numpy as np
import trimesh
from tqdm import tqdm


def generate_heightmap(mesh, xy_range=((0, 8), (0, 8)), resolution=30, ray_offset=0.01):
    """
    Generate a heightmap from a mesh within a specified XY range and resolution, with improved ray casting.

    Parameters:
    - mesh: Trimesh object, the mesh to sample.
    - xy_range: tuple of tuples, specifying the ((min_x, max_x), (min_y, max_y)) range in meters.
    - resolution: float, resolution in points per meter.
    - ray_offset: float, the distance to offset additional rays around the primary ray to avoid precision issues.

    Returns:
    - heightmap: 2D NumPy array, the generated heightmap.
    """
    (min_x, max_x), (min_y, max_y) = xy_range
    width = int((max_x - min_x) * resolution)
    height = int((max_y - min_y) * resolution)
    iX = int(min_x * resolution)
    iY = int(min_y * resolution)

    # Calculate the Z start point (above the highest point of the mesh)
    z_start = (
        mesh.bounds[:, 2].max() + 10
    )  # Start from 10 units above the highest point in the mesh

    # Offsets for rays in a small pattern around each X, Y position
    offsets = [
        (0, 0),
        (ray_offset, 0),
        (-ray_offset, 0),
        (0, ray_offset),
        (0, -ray_offset),
        (ray_offset, ray_offset),
        (-ray_offset, -ray_offset),
        (-ray_offset, ray_offset),
        (ray_offset, -ray_offset),
    ]

    # Initialize the heightmap arrays
    X, Y = np.meshgrid(range(iX, iX + width), range(iY, iY + height))
    heightmap = np.ones_like(X.transpose()) * -np.inf
    heightmap[[0, -1], :] = 0.0
    heightmap[:, [0, -1]] = 0.0

    # Calculate the XY coordinates from where the rays are launched
    ray_origins = np.array(
        [
            X[1:-1, 1:-1].ravel() / resolution,
            Y[1:-1, 1:-1].ravel() / resolution,
            np.ones((width - 2) * (height - 2)) * z_start,
        ]
    ).transpose()

    # Cast a ray downwards from above the mesh
    ray_directions = np.tile(np.array([[0, 0, -1]]), ((width - 2) * (height - 2), 1))

    for dx, dy in tqdm(offsets):
        # Check for intersections
        locations, index_ray, index_tri = mesh.ray.intersects_location(
            ray_origins=ray_origins + np.array([dx, dy, 0.0]) / resolution,
            ray_directions=ray_directions,
            multiple_hits=False,
        )

        # Keep maximum height over tested offsets
        fidx = (locations[:, :2] * resolution).astype(np.int64) - np.array([iX, iY])
        heightmap[fidx[:, 0], fidx[:, 1]] = np.maximum(
            heightmap[fidx[:, 0], fidx[:, 1]], locations[:, 2]
        )

    return heightmap.transpose()


import matplotlib.pyplot as plt


def plot_heightmap(heightmap, xy_range=((0, 8), (0, 8)), filename=None):
    """
    Plot the heightmap using matplotlib. Optionally, save the plot to a file.

    Parameters:
    - heightmap: 2D NumPy array, the heightmap to plot.
    - xy_range: tuple of tuples, specifying the ((min_x, max_x), (min_y, max_y)) range in meters.
    - filename: Optional; if provided, the plot is saved to this file as a PNG. Otherwise, the plot is displayed.
    """
    (min_x, max_x), (min_y, max_y) = xy_range

    # Set up the figure and axis for plotting
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot the heightmap
    c = ax.imshow(
        heightmap, extent=(min_x, max_x, min_y, max_y), origin="lower", cmap="terrain"
    )

    # Add a colorbar to the plot to show the height scale
    fig.colorbar(c, ax=ax, label="Height (m)")

    # Set plot labels and title
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Heightmap")

    # Save to file if filename is provided, otherwise show the plot
    if filename:
        plt.savefig(filename, format="png")
        plt.close()  # Close the figure to prevent it from displaying in the notebook
    else:
        plt.show()


if __name__ == "__main__":
    # Usage:
    xy_range = ((0, 8), (0, 8))
    resolution = 5
    from terrain_stairs import *

    mesh = generate_pyramid_stairs_terrain()
    # Generate the heightmap
    heightmap = generate_heightmap(mesh, xy_range, resolution)
    plot_heightmap(heightmap, xy_range)
