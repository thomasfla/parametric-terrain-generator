import generators.terrain_generators as tgen
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
params["borderSize"] = 2.5
params["numLevels"] = 4
params["numTerrains"] = 5
params["resolution"] = 100

terrainProportions = {}
terrainProportions["stairs_upwards"] = 1.0
terrainProportions["stairs_downwards"] = 1.0
terrainProportions["slope_upwards"] = 1.0
terrainProportions["random_blocks"] = 1.0
terrainProportions["perlin"] = 1.0
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

print("-- Terrain generation --")
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

# Add border
meshes.append(
    tgen.create_border(
        params["terrainSize"] * params["numLevels"],
        params["terrainSize"] * params["numTerrains"],
        params["borderSize"],
    )
)

world_mesh = trimesh.util.concatenate(meshes)

# Display mesh with colormap along the Z axis
world_mesh.visual.vertex_colors = trimesh.visual.interpolate(
    world_mesh.vertices[:, 2], color_map="terrain"
)
scene = trimesh.Scene(world_mesh)
# scene.show()

data = scene.save_image(resolution=[1920, 1080], visible=False)
time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
fn = "images/terrains_" + time_str + ".png"
with open(fn, "wb") as f:
    f.write(data)
fn = "images/last_concatenated_terrains.png"
with open(fn, "wb") as f:
    f.write(data)

######
# Heightmap generation
######

print("-- Heightmap generation --")
hm = generate_heightmap(
    world_mesh,
    xy_range=(
        (
            -params["borderSize"],
            params["numLevels"] * params["terrainSize"] + params["borderSize"],
        ),
        (
            -params["borderSize"],
            params["numTerrains"] * params["terrainSize"] + params["borderSize"],
        ),
    ),
    resolution=params["resolution"],
)

fn = "images/terrains_" + time_str + "_heightmap.png"
plot_heightmap(
    hm,
    xy_range=(
        (
            -params["borderSize"],
            params["terrainSize"] * params["numLevels"] + params["borderSize"],
        ),
        (
            -params["borderSize"],
            params["terrainSize"] * params["numTerrains"] + params["borderSize"],
        ),
    ),
    filename=fn,
)

######
# Heightmap generation
######

print("--Saving mesh, heightmap and parameters --")
np.savez(
    "data/terrain_" + time_str + ".npz",
    vertices=world_mesh.vertices,
    triangles=world_mesh.faces,
    heightmap=hm.transpose(),
    params=params,
)

print("-- Done --")
