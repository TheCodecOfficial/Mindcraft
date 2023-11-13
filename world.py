from settings import *
from objects.chunk import Chunk
from voxel_interaction import VoxelInteraction
import random
import heapq


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = {}
        # self.chunks = [None] * WORLD_VOL
        # self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype=np.uint8)
        self.build_chunks()
        self.build_chunk_meshes()
        self.voxel_interaction = VoxelInteraction(self)

        self.chunks_to_generate = []

        self.player = self.app.player
        self.player.functions_to_call.append(self.load_chunks_around_player)
        self.player.functions_to_call.append(self.cleanup_chunks)

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
        if self.chunk_exists(x, y, z):
            return

        # print(f"Generating chunk [{x}, {y}, {z}]")
        chunk = Chunk(self, (x, y, z))
        self.chunks[(x, y, z)] = chunk
        chunk.build_mesh()

    def chunk_exists(self, x, y, z):
        return (x, y, z) in self.chunks

    def build_chunk_meshes(self):
        for chunk in self.chunks.values():
            chunk.build_mesh()

    def load_chunks_around_player(self):
        playerpos = self.player.camera.position
        chunkpos = glm.ivec3(playerpos) // CHUNK_SIZE
        x = chunkpos.x
        y = chunkpos.y
        z = chunkpos.z
        r = GENERATE_DISTANCE
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    chunk_coords = (x + dx, y + dy, z + dz)
                    if not self.chunk_exists(*chunk_coords):
                        dist = dx * dx + dy * dy + dz * dz
                        heapq.heappush(self.chunks_to_generate, (dist, chunk_coords))

    def test(self):
        print("TESTING")

    def cleanup_chunks(self):
        self.chunks_to_generate = self.chunks_to_generate[:1000]

    def update(self):
        l = len(self.chunks_to_generate)
        if l != 0:
            print(f"Chunks to generate: {l}")
            pass
        for i in range(2):
            if self.chunks_to_generate:
                chunk_coords = heapq.heappop(self.chunks_to_generate)[1]
                self.generate_chunk(*chunk_coords)
        #self.load_chunks_around_player()
        self.voxel_interaction.update()

    def render(self):
        for chunk_coords, chunk in self.chunks.items():
            world_coords = glm.vec3(chunk_coords) * CHUNK_SIZE
            distance = glm.distance(world_coords, self.player.camera.position)
            if distance / CHUNK_SIZE <= RENDER_DISTANCE:
                chunk.render()