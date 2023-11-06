from settings import *
from objects.chunk import Chunk
from voxel_interaction import VoxelInteraction
import random


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = [None] * WORLD_VOL
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype=np.uint8)
        self.build_chunks()
        self.build_chunk_meshes()
        self.voxel_interaction = VoxelInteraction(self)

    def build_chunks(self):
        for x in range(WORLD_WIDTH):
            for z in range(WORLD_DEPTH):
                for y in range(WORLD_HEIGHT):
                    chunk = Chunk(self, (x, y, z))
                    chunk_index = x + z * WORLD_WIDTH + y * WORLD_AREA
                    self.chunks[chunk_index] = chunk

                    self.voxels[chunk_index] = chunk.build_voxels()
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_meshes(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_interaction.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()
