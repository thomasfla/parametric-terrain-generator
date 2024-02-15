from terrain_perlin import generate_perlin_terrain
from terrain_stairs import generate_pyramid_stairs_terrain
from terrain_blocks import generate_block_terrain
from terrain_heightmap import *
from PIL import Image
import trimesh
from IPython import embed
import numpy as np

mesh = generate_pyramid_stairs_terrain()

# Create a scene from the mesh if not already done

# embed()

meshs = []
meshs.append(generate_perlin_terrain())
meshs.append(generate_pyramid_stairs_terrain(going_up=False))
meshs.append(generate_pyramid_stairs_terrain(going_up=True))
meshs.append(generate_step_field_terrain())
i = 0
for mesh in meshs:
    i += 1
    mesh.visual.vertex_colors = trimesh.visual.interpolate(
        mesh.vertices[:, 2], color_map="terrain"
    )
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
    fn = "terrain{}_3d.png".format(i)
    with open(fn, "wb") as f:
        f.write(data)
    hm = generate_heightmap(mesh, resolution=10)
    fn = "terrain{}_heightmap.png".format(i)

    plot_heightmap(hm, filename=fn)
