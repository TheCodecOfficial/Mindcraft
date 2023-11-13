from settings import *
import numpy as np
from meshes.mesh import Mesh
from meshes.chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(Mesh):
    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.shader = self.app.shader_program.chunk_shader
        self.world_utils = chunk.world.utils

        self.vbo_format = "1u4"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("packed_vertex_data",)
        self.vao = self.get_vao()

    def rebuild_mesh(self):
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        chunk_voxels = [self.chunk.voxels] * 27
        cx, cy, cz = self.chunk.position
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    index = (x + 1) + (y + 1) * 9 + (z + 1) * 3
                    chunk_voxels[index] = self.world_utils.get_chunk_voxels(
                        cx + x, cy + y, cz + z, return_empty=True
                    )

        mesh = build_chunk_mesh(
            chunk_voxels,
            self.chunk.position,
            self.format_size,
        )
        return mesh
