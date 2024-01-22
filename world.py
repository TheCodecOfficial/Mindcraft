from settings import *
from objects.chunk import Chunk
from voxel_interaction import VoxelInteraction
import random
import heapq
import sys


class World:
    def __init__(self, app):
        self.app = app
        self.chunks = {}
        self.utils = WorldUtils(self)
        self.build_chunks()
        self.build_chunk_meshes()
        self.voxel_interaction = VoxelInteraction(self)

        self.chunks_to_generate = []

        self.player = self.app.player
        self.player.functions_to_call.append(self.load_chunks_around_player)
        self.player.functions_to_call.append(self.cleanup_chunks)

        # self.generate_chunk(10, 0, 0)

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

        coords = [
            (0, 0, 0),
            (-2, 5, -1),
            (-3, 5, -1),
            (-2, 4, -1),
            (-2, 5, -2),
            (-2, 5, 0),
            (-2, 6, -1),
            (-1, 5, -1),
            (-3, 4, -1),
            (-3, 5, -2),
            (-3, 5, 0),
            (-3, 6, -1),
            (-2, 4, -2),
            (-2, 4, 0),
            (-2, 6, -2),
            (-2, 6, 0),
            (-1, 4, -1),
            (-1, 5, -2),
            (-1, 5, 0),
            (-1, 6, -1),
            (-3, 4, -2),
            (-3, 4, 0),
            (-3, 6, -2),
            (-3, 6, 0),
            (-1, 4, -2),
            (-1, 4, 0),
            (-1, 6, -2),
            (-1, 6, 0),
            (-4, 5, -1),
            (-2, 3, -1),
            (-2, 7, -1),
            (0, 5, -1),
            (-4, 4, -1),
            (-4, 5, -2),
            (-4, 5, 0),
            (-4, 6, -1),
            (-3, 3, -1),
            (-3, 7, -1),
            (-2, 3, -2),
            (-2, 3, 0),
            (-2, 7, -2),
            (-2, 7, 0),
            (-1, 3, -1),
            (-1, 7, -1),
            (0, 4, -1),
            (0, 5, -2),
            (0, 5, 0),
            (0, 6, -1),
            (-4, 4, -2),
            (-4, 4, 0),
            (-4, 6, -2),
            (-4, 6, 0),
            (-3, 3, -2),
            (-3, 3, 0),
            (-3, 7, -2),
            (-3, 7, 0),
            (-1, 3, -2),
            (-1, 3, 0),
            (-1, 7, -2),
            (-1, 7, 0),
            (0, 4, -2),
            (0, 4, 0),
            (0, 6, -2),
            (0, 6, 0),
            (-4, 3, -1),
            (-4, 7, -1),
            (0, 3, -1),
            (0, 7, -1),
            (-5, 5, -1),
            (-4, 3, -2),
            (-4, 3, 0),
            (-4, 7, -2),
            (-4, 7, 0),
            (-2, 2, -1),
            (-2, 8, -1),
            (0, 3, -2),
            (0, 3, 0),
            (0, 7, -2),
            (0, 7, 0),
            (1, 5, -1),
            (-5, 4, -1),
            (-5, 5, -2),
            (-5, 5, 0),
            (-5, 6, -1),
            (-3, 2, -1),
            (-3, 8, -1),
            (-2, 2, -2),
            (-2, 2, 0),
            (-2, 8, -2),
            (-2, 8, 0),
            (-1, 2, -1),
            (-1, 8, -1),
            (1, 4, -1),
            (1, 5, -2),
            (1, 5, 0),
            (1, 6, -1),
            (-5, 4, -2),
            (-5, 4, 0),
            (-5, 6, -2),
            (-5, 6, 0),
            (-3, 2, -2),
            (-3, 2, 0),
            (-3, 8, -2),
            (-3, 8, 0),
            (-1, 2, -2),
            (-1, 2, 0),
            (-1, 8, -2),
            (-1, 8, 0),
            (1, 4, -2),
            (1, 4, 0),
            (1, 6, -2),
            (1, 6, 0),
            (-5, 3, -1),
            (-5, 7, -1),
            (-4, 2, -1),
            (-4, 8, -1),
            (0, 2, -1),
            (0, 8, -1),
            (1, 3, -1),
            (1, 7, -1),
            (-5, 3, -2),
            (-5, 3, 0),
            (-5, 7, -2),
            (-5, 7, 0),
            (-4, 2, -2),
            (-4, 2, 0),
            (-4, 8, -2),
            (-4, 8, 0),
            (0, 2, -2),
            (0, 2, 0),
            (0, 8, -2),
            (0, 8, 0),
            (1, 3, -2),
            (1, 3, 0),
            (1, 7, -2),
            (1, 7, 0),
            (-6, 5, -1),
            (-2, 1, -1),
            (-2, 9, -1),
            (2, 5, -1),
            (-6, 4, -1),
            (-6, 5, -2),
            (-6, 5, 0),
            (-6, 6, -1),
            (-3, 1, -1),
            (-3, 9, -1),
            (-2, 1, -2),
            (-2, 1, 0),
            (-2, 9, -2),
            (-2, 9, 0),
            (-1, 1, -1),
            (-1, 9, -1),
            (2, 4, -1),
            (2, 5, -2),
            (2, 5, 0),
            (2, 6, -1),
            (-6, 4, -2),
            (-6, 4, 0),
            (-6, 6, -2),
            (-6, 6, 0),
            (-5, 2, -1),
            (-5, 8, -1),
            (-3, 1, -2),
            (-3, 1, 0),
            (-3, 9, -2),
            (-3, 9, 0),
            (-1, 1, -2),
            (-1, 1, 0),
            (-1, 9, -2),
            (-1, 9, 0),
            (1, 2, -1),
            (1, 8, -1),
            (2, 4, -2),
            (2, 4, 0),
            (2, 6, -2),
            (2, 6, 0),
            (-5, 2, -2),
            (-5, 2, 0),
            (-5, 8, -2),
            (-5, 8, 0),
            (1, 2, -2),
            (1, 2, 0),
            (1, 8, -2),
            (1, 8, 0),
            (-6, 3, -1),
            (-6, 7, -1),
            (-4, 1, -1),
            (-4, 9, -1),
            (0, 1, -1),
            (0, 9, -1),
            (2, 3, -1),
            (2, 7, -1),
            (-6, 3, -2),
            (-6, 3, 0),
            (-6, 7, -2),
            (-6, 7, 0),
            (-4, 1, -2),
            (-4, 1, 0),
            (-4, 9, -2),
            (-4, 9, 0),
            (0, 1, -2),
            (0, 1, 0),
            (0, 9, -2),
            (0, 9, 0),
            (2, 3, -2),
            (2, 3, 0),
            (2, 7, -2),
            (2, 7, 0),
            (-6, 2, -1),
            (-6, 8, -1),
            (-5, 1, -1),
            (-5, 9, -1),
            (1, 1, -1),
            (1, 9, -1),
            (2, 2, -1),
            (2, 8, -1),
            (-6, 2, -2),
            (-6, 2, 0),
            (-6, 8, -2),
            (-6, 8, 0),
            (-5, 1, -2),
            (-5, 1, 0),
            (-5, 9, -2),
            (-5, 9, 0),
            (1, 1, -2),
            (1, 1, 0),
            (1, 9, -2),
            (1, 9, 0),
            (2, 2, -2),
            (2, 2, 0),
            (2, 8, -2),
            (2, 8, 0),
            (-6, 1, -1),
            (-6, 9, -1),
            (2, 1, -1),
            (2, 9, -1),
            (-6, 1, -2),
            (-6, 1, 0),
            (-6, 9, -2),
            (-6, 9, 0),
            (2, 1, -2),
            (2, 1, 0),
            (2, 9, -2),
            (2, 9, 0),
            (-2, 5, 1),
            (-3, 5, 1),
            (-2, 4, 1),
            (-2, 6, 1),
            (-1, 5, 1),
            (-3, 4, 1),
            (-3, 6, 1),
            (-1, 4, 1),
            (-1, 6, 1),
            (-4, 5, 1),
            (-2, 3, 1),
            (-2, 7, 1),
            (0, 5, 1),
            (-4, 4, 1),
            (-4, 6, 1),
            (-3, 3, 1),
            (-3, 7, 1),
            (-1, 3, 1),
            (-1, 7, 1),
            (0, 4, 1),
            (0, 6, 1),
            (1, 5, 1),
            (0, 3, 1),
            (0, 7, 1),
            (1, 4, 1),
            (1, 6, 1),
            (-4, 3, 1),
            (-4, 7, 1),
            (1, 3, 1),
            (1, 7, 1),
            (-5, 5, 1),
            (-2, 2, 1),
            (-2, 8, 1),
            (-1, 2, 1),
            (-1, 8, 1),
            (2, 5, 1),
            (-5, 4, 1),
            (-5, 6, 1),
            (-3, 2, 1),
            (-3, 8, 1),
            (0, 2, 1),
            (0, 8, 1),
            (2, 4, 1),
            (2, 6, 1),
            (-5, 3, 1),
            (-5, 7, 1),
            (-4, 2, 1),
            (-4, 8, 1),
            (1, 2, 1),
            (1, 8, 1),
            (2, 3, 1),
            (2, 7, 1),
            (3, 5, 0),
            (-6, 5, 1),
            (-2, 1, 1),
            (-2, 9, 1),
            (-1, 1, 1),
            (-1, 9, 1),
            (3, 4, 0),
            (3, 5, -1),
            (3, 5, 1),
            (3, 6, 0),
            (-6, 4, 1),
            (-6, 6, 1),
            (-3, 1, 1),
            (-3, 9, 1),
            (0, 1, 1),
            (0, 9, 1),
            (3, 4, -1),
            (3, 4, 1),
            (3, 6, -1),
            (3, 6, 1),
            (-5, 2, 1),
            (-5, 8, 1),
            (2, 2, 1),
            (2, 8, 1),
            (3, 3, 0),
            (3, 7, 0),
            (-6, 3, 1),
            (-6, 7, 1),
            (-4, 1, 1),
            (-4, 9, 1),
            (1, 1, 1),
            (1, 9, 1),
            (3, 3, -1),
            (3, 3, 1),
            (3, 7, -1),
            (3, 7, 1),
            (3, 2, 0),
            (3, 8, 0),
            (-6, 2, 1),
            (-6, 8, 1),
            (-5, 1, 1),
            (-5, 9, 1),
            (2, 1, 1),
            (2, 9, 1),
            (3, 2, -1),
            (3, 2, 1),
            (3, 8, -1),
            (3, 8, 1),
            (3, 1, 0),
            (3, 9, 0),
            (-6, 1, 1),
            (-6, 9, 1),
            (3, 1, -1),
            (3, 1, 1),
            (3, 9, -1),
            (3, 9, 1),
            (3, 5, -2),
            (3, 4, -2),
            (3, 6, -2),
            (3, 3, -2),
            (3, 7, -2),
            (3, 2, -2),
            (3, 8, -2),
            (3, 1, -2),
            (3, 9, -2),
            (4, 5, -1),
            (4, 4, -1),
            (4, 5, -2),
            (4, 5, 0),
            (4, 6, -1),
            (4, 4, -2),
            (4, 4, 0),
            (4, 6, -2),
            (4, 6, 0),
            (4, 3, -1),
            (4, 7, -1),
            (4, 3, -2),
            (4, 3, 0),
            (4, 7, -2),
            (4, 7, 0),
            (4, 2, -1),
            (4, 8, -1),
            (4, 2, -2),
            (4, 2, 0),
            (4, 8, -2),
            (4, 8, 0),
            (4, 1, -1),
            (4, 9, -1),
            (4, 1, -2),
            (4, 1, 0),
            (5, 5, -1),
            (5, 4, -1),
            (5, 5, -2),
            (5, 5, 0),
            (5, 6, -1),
            (5, 4, -2),
            (5, 4, 0),
            (5, 6, -2),
            (5, 6, 0),
            (5, 3, -1),
            (5, 7, -1),
            (5, 3, -2),
            (5, 3, 0),
            (5, 7, -2),
            (5, 7, 0),
            (5, 2, -1),
            (5, 8, -1),
            (4, 9, -2),
            (4, 9, 0),
            (5, 2, -2),
            (5, 2, 0),
            (5, 8, -2),
            (5, 8, 0),
            (5, 1, -1),
            (5, 9, -1),
            (5, 1, -2),
            (5, 1, 0),
            (5, 9, -2),
            (5, 9, 0),
        ]
        for x, y, z in coords:
            print(f"Building chunk {i}/{WORLD_VOL} [{x}, {y}, {z}]")
            chunk = Chunk(self, (x, y, z))
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
        print(f"Total chunks: {len(self.chunks)}")
        print(f"Total approx voxels: {len(self.chunks) * CHUNK_VOL}")

        # return
        playerpos = self.player.camera.position
        chunkpos = glm.ivec3(playerpos) // CHUNK_SIZE
        x = chunkpos.x
        y = chunkpos.y
        z = chunkpos.z
        r = GENERATE_DISTANCE
        rz = r // 4
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for dz in range(-rz, rz + 1):
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
            # print(f"Chunks to generate: {l}")
            pass
        num_at_once = 1
        for _ in range(num_at_once):
            if self.chunks_to_generate:
                chunk_coords = heapq.heappop(self.chunks_to_generate)[1]
                self.utils.rebuild_chunks_around(*chunk_coords)
                self.generate_chunk(*chunk_coords)

        self.voxel_interaction.update()

    def render(self):
        for chunk_coords, chunk in self.chunks.items():
            world_coords = glm.vec3(chunk_coords) * CHUNK_SIZE
            distance = glm.distance(world_coords, self.player.camera.position)
            if distance / CHUNK_SIZE <= RENDER_DISTANCE:
                chunk.render()


class WorldUtils:
    def __init__(self, world):
        self.world = world
        self.chunks = world.chunks

    def chunk_exists(self, x, y, z):
        return (x, y, z) in self.chunks.keys()

    def get_chunk(self, x, y, z):
        if self.chunk_exists(x, y, z):
            return self.chunks[(x, y, z)]

        return None

    def get_chunk_voxels(self, x, y, z, return_empty=False):
        if self.chunk_exists(x, y, z):
            return self.chunks[(x, y, z)].voxels
        elif return_empty:
            return np.zeros(CHUNK_VOL, dtype=np.uint8)

        return None

    def rebuild_chunk(self, x, y, z):
        chunk = self.get_chunk(x, y, z)
        if chunk:
            chunk.build_mesh()

    def rebuild_chunks_around(self, x, y, z):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    self.rebuild_chunk(x + dx, y + dy, z + dz)
