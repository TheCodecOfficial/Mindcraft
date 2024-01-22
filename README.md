# Modular Infinite Network of Dynamic Cubic Realms And Fractal Terrain (MINDCRAFT)

## Features
### Chunk Datastructure
The world is split up into chunks of 32x32x32 voxels. Chunks are stored in a dictionary with their coordinates as keys. This allows for infinite worlds, as chunks are only generated when they are needed. All chunks in a given generation radius around the player are generated, starting at the closest to the player and moving outwards. Chunk culling is used to only render chunks that are visible to the player. 

Another benefit of seperating the world into chunks is that each chunk can be rendered as a single mesh, which is much more efficient than rendering each voxel individually. When voxels are added, modified or removed, only the mesh of the chunk that contains the voxel is updated (and the meshes of the neighbouring chunks, if the voxel is on the edge of the chunk).
### Shading
![](screenshots/no%20shading.png)
### Terrain Generation


## Acknowledgments

Parts of the engine follow this [tutorial](https://www.youtube.com/watch?v=Ab8TOSFfNp4) on YouTube.

- [Amanatides, John & Woo, Andrew. (1987). A Fast Voxel Traversal Algorithm for Ray Tracing](http://www.cse.yorku.ca/~amana/research/grid.pdf)

#### Installation

1. `pip install pygame moderngl PyGLM numba opensimplex`
2. Run `main.py`
