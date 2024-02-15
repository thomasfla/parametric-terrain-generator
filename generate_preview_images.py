from terrain_heightmap import generate_heightmap, plot_heightmap
import trimesh
import numpy as np
from tqdm import tqdm

print("-- Generating meshes --")
meshs = []
meshs.append(generate_perlin_terrain())
meshs.append(generate_pyramid_stairs_terrain(going_up=False))
meshs.append(generate_pyramid_stairs_terrain(going_up=True))
meshs.append(generate_block_terrain())

print("-- Generating images and heightmaps --")
for i, mesh in enumerate(tqdm(meshs)):
    # Add colormap to mesh along z coordinate
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="terrain"
    )

    # Create a scene from the mesh
    scene = trimesh.Scene(mesh)
    camera_transform = np.array(
        [
            [0.99450777, -0.00839196, 0.10432578, 5.05440546],
            [0.09607263, 0.46867095, -0.87813301, -4.87516238],
            [-0.0415252, 0.88333296, 0.46690314, 4.26892199],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    # Apply the generated transform to the scene's camera
    scene.camera_transform = camera_transform

    # Save the scene to an image
    data = scene.save_image(resolution=[1920, 1080], visible=False)

    # Convert the image data to an actual image and save it
    fn = "terrain{}_3d.png".format(i + 1)
    with open(fn, "wb") as f:
        f.write(data)
    hm = generate_heightmap(mesh, resolution=10)
    fn = "terrain{}_heightmap.png".format(i + 1)

    plot_heightmap(hm, filename=fn)
