from settings import *
from meshes.chunk_mesh import ChunkMesh


class Chunk:
    def __init__(self, app):
        self.app = app
        self.voxels: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        self.mesh.render()

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = x + y + z if int(glm.simplex(glm.vec3(x, y, z) * 0.1) + 1) else 0
        return voxels
