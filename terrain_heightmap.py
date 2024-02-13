import matplotlib.pyplot as plt
import numpy as np
import trimesh
def generate_heightmap(mesh, xy_range, resolution, ray_offset=0.01):
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

    # Initialize the heightmap array
    heightmap = np.full((height, width), np.nan)

    # Calculate the Z start point (above the highest point of the mesh)
    z_start = mesh.bounds[:, 2].max() + 10  # Start from 10 units above the highest point in the mesh

    # Offsets for rays in a small pattern around each X, Y position
    offsets = [(0, 0), (ray_offset, 0), (-ray_offset, 0), (0, ray_offset), (0, -ray_offset)]

    for i in range(width):
        for j in range(height):
            highest_z = None
            for dx, dy in offsets:
                # Calculate the XY coordinates with offset
                x = min_x + (i + dx) / resolution
                y = min_y + (j + dy) / resolution

                # Cast a ray downwards from above the mesh
                ray_origins = np.array([[x, y, z_start]])
                ray_directions = np.array([[0, 0, -1]])  # Downwards

                # Check for intersections
                locations, index_ray, index_tri = mesh.ray.intersects_location(
                    ray_origins=ray_origins,
                    ray_directions=ray_directions)
                
                # Update the highest Z-coordinate found
                if len(locations) > 0:
                    max_z = locations[:, 2].max()
                    if highest_z is None or max_z > highest_z:
                        highest_z = max_z
            
            # Set the heightmap value if an intersection was found
            if highest_z is not None:
                heightmap[j, i] = highest_z

    return heightmap


def plot_heightmap(heightmap, xy_range):
    """
    Plot the heightmap using matplotlib.

    Parameters:
    - heightmap: 2D NumPy array, the heightmap to plot.
    - xy_range: tuple of tuples, specifying the ((min_x, max_x), (min_y, max_y)) range in meters.
    """
    (min_x, max_x), (min_y, max_y) = xy_range

    # Set up the figure and axis for plotting
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot the heightmap
    # Note: The origin='lower' argument makes the first row in the array appear at the bottom of the plot.
    c = ax.imshow(heightmap, extent=(min_x, max_x, min_y, max_y), origin='lower', cmap='terrain')
    
    # Add a colorbar to the plot to show the height scale
    fig.colorbar(c, ax=ax, label='Height (m)')

    # Set plot labels and title
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Heightmap')

    # Show the plot
    plt.show()



#Usage: 
xy_range = ((0, 8), (0, 8)) 
resolution = 30  
from terrain_stairs import *
mesh = generate_pyramid_stairs_terrain()
# Generate the heightmap
heightmap = generate_heightmap(mesh, xy_range, resolution)
plot_heightmap(heightmap, xy_range)