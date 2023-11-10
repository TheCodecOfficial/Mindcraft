from settings import *
from world import World
from meshes.chunk_mesh_builder import get_chunk_index


class WorldUtil:
    def __init__(self, app):
        self.app = app
        self.chunks = app.scene.world.chunks

    def get_chunk_index(self, x, y, z):
        return int(get_chunk_index((x, y, z)))

    def get_chunk_coords(self, x, y, z):
        chunk_index = self.get_chunk_index(x, y, z)
        chunk_y = chunk_index // (WORLD_WIDTH * WORLD_DEPTH)
        chunk_z = (chunk_index // WORLD_WIDTH) % WORLD_DEPTH
        chunk_x = chunk_index % WORLD_WIDTH
        return chunk_x, chunk_y, chunk_z

    def get_local_coords(self, x, y, z):
        chunk_x, chunk_y, chunk_z = self.get_chunk_coords(x, y, z)
        local_x = x - chunk_x * CHUNK_SIZE
        local_y = y - chunk_y * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE
        return local_x, local_y, local_z

    def get_voxel_index(self, x, y, z):
        local_x, local_y, local_z = self.get_local_coords(x, y, z)
        return int(int(local_x) + int(local_z) * CHUNK_SIZE + int(local_y) * CHUNK_AREA)

    def get_voxel_id(self, x, y, z):
        voxel_index = self.get_voxel_index(x, y, z)
        chunk_index = self.get_chunk_index(x, y, z)
        if -1 < chunk_index < WORLD_VOL:
            chunk = self.chunks[chunk_index]
            if -1 < voxel_index < CHUNK_VOL:
                voxel_id = chunk.voxels[voxel_index]
                return voxel_id
        return -1

    def is_void(self, x, y, z):
        voxel_id = self.get_voxel_id(x, y, z)
        return voxel_id == 0 or voxel_id == -1
    
    def is_occupied(self, x, y, z):
        return not self.is_void(x, y, z)
    
    def get_height(self, x, y, z):
        height = 0
        while self.get_voxel_id(x, y, z) == 0:
            height += 1
            y -= 1

        return height
