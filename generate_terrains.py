import terrain_generators as tgen
from terrain_heightmap import generate_heightmap, plot_heightmap
import trimesh
import numpy as np
from tqdm import tqdm
from datetime import datetime

######
# Parameters of terrain generation
######

params = {}
params["terrainSize"] = 8.0
params["borderSize"] = 10.0
params["numLevels"] = 3
params["numTerrains"] = 4
params["resolution"] = 0.01

terrainProportions = {}
terrainProportions["stairs_upwards"] = 0.25
terrainProportions["stairs_downwards"] = 0.25
terrainProportions["blocks"] = 0.25
terrainProportions["perlin"] = 0.25
params["terrainProportions"] = terrainProportions

params["info"] = []

######
# Prepare generators
######

csum = 0
tgens = []
tgens_csum = []
for name in terrainProportions.keys():
    if terrainProportions[name] > 0:
        tgens.append(getattr(tgen, name))
        csum += terrainProportions[name]
        tgens_csum.append(csum)

if len(tgens) == 0:
    print("At least one terrain type must be enabled.")

# Normalizing the terrain proportions
tgens_csum = np.array(tgens_csum) / tgens_csum[-1]

######
# Terrain generation
######

meshes = []
difficulties = np.linspace(0, 1, params["numLevels"])
for i in tqdm(range(params["numTerrains"])):
    # Choice of terrain type
    k = np.argwhere(i / params["numTerrains"] < tgens_csum)[0, 0]

    for j in range(params["numLevels"]):
        # Generate the mesh for given difficulty
        mesh, info = tgens[k](difficulties[j])

        # Place the mesh in the world
        center = [j * params["terrainSize"], i * params["terrainSize"]]
        shift_matrix = np.eye(4)
        shift_matrix[:2, -1] = center[0], center[1]
        mesh.apply_transform(shift_matrix)

        # Save mesh and info
        meshes.append(mesh)
        if j == 0:
            params["info"].append(info)

world_mesh = trimesh.util.concatenate(meshes)

# Display mesh with colormap along the Z axis
world_mesh.visual.vertex_colors = trimesh.visual.interpolate(
    world_mesh.vertices[:, 2], color_map="viridis"
)
scene = trimesh.Scene(world_mesh)
data = scene.save_image(resolution=[1920, 1080], visible=False)
time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
fn = "images/terrains_" + time_str + ".png"
with open(fn, "wb") as f:
    f.write(data)

quit()

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
    fn = "images/terrain{}_3d.png".format(i + 1)
    with open(fn, "wb") as f:
        f.write(data)
    hm = generate_heightmap(mesh, resolution=10)
    fn = "images/terrain{}_heightmap.png".format(i + 1)

    plot_heightmap(hm, filename=fn)
