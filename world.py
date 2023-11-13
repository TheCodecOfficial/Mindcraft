from settings import *
from objects.chunk import Chunk
from voxel_interaction import VoxelInteraction
import random


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = {}
        # self.chunks = [None] * WORLD_VOL
        # self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype=np.uint8)
        self.build_chunks()
        self.build_chunk_meshes()
        self.voxel_interaction = VoxelInteraction(self)

        self.player = self.app.player

        self.generate_chunk(10, 0, 0)

    def build_chunks(self):
        i = 0
        for x in range(WORLD_WIDTH):
            for z in range(WORLD_DEPTH):
                for y in range(WORLD_HEIGHT):
                    i += 1
                    print(f"Building chunk {i}/{WORLD_VOL} [{x}, {y}, {z}]")
                    chunk = Chunk(self, (x, y, z))
                    # chunk_index = x + z * WORLD_WIDTH + y * WORLD_AREA
                    self.chunks[(x, y, z)] = chunk

    def generate_chunk(self, x, y, z):
        if (x, y, z) in self.chunks:
            return

        print(f"Generating chunk [{x}, {y}, {z}]")
        chunk = Chunk(self, (x, y, z))
        self.chunks[(x, y, z)] = chunk
        chunk.build_mesh()

    def build_chunk_meshes(self):
        for chunk in self.chunks.values():
            chunk.build_mesh()

    def load_chunks_around_player(self):
        playerpos = self.player.camera.position
        chunkpos = glm.ivec3(playerpos) // CHUNK_SIZE
        x = chunkpos.x
        y = chunkpos.y
        z = chunkpos.z
        r = 2
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    self.generate_chunk(x + dx, y + dy, z + dz)

    def update(self):
        self.load_chunks_around_player()
        self.voxel_interaction.update()

    def render(self):
        for chunk in self.chunks.values():
            chunk.render()
