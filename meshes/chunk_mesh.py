import numpy as np
from meshes.mesh import Mesh
from meshes.chunk_mesh_builder import build_chunk_mesh


class ChunkMesh(Mesh):
    def __init__(self, chunk):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.shader = self.app.shader_program.chunk

        self.vbo_format = "3u1 1u1 1u1"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_position", "voxel_id", "face_dir")
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        mesh = build_chunk_mesh(
            self.chunk.voxels,
            self.format_size,
            self.chunk.position,
            self.chunk.world.voxels, # TODO: This seems weird
        )
        return mesh
