from settings import *
import random
from meshes.chunk_mesh_builder import get_chunk_index


class VoxelInteraction:
    def __init__(self, world):
        self.app = world.app
        self.chunks = world.chunks

        # ray casting result
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None

        self.interaction_mode = 0  # 0: remove voxel   1: add voxel
        self.new_voxel_id = 1

    def add_voxel(self):
        if self.voxel_id:
            voxel_id = self.get_voxel_id(self.voxel_world_pos + self.voxel_normal)
            voxel_id, voxel_index, _, chunk = voxel_id
            if not voxel_id:
                chunk.voxels[voxel_index] = random.randint(1, 255)
                self.chunk.mesh.rebuild_mesh()

                chunk.is_empty = False

    def remove_voxel(self):
        if self.voxel_id:
            self.chunk.voxels[self.voxel_index] = 0
            self.chunk.mesh.rebuild_mesh()

    def set_voxel(self):
        if self.interaction_mode:
            self.add_voxel()
        else:
            self.remove_voxel()

        self.rebuild_adjacent_chunks()

    def rebuild_chunk(self, index):
        if index != -1:
            self.chunks[index].mesh.rebuild_mesh()

    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        chunk_index = -1
        if lx == 0:
            chunk_index = get_chunk_index((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            chunk_index = get_chunk_index((wx + 1, wy, wz))

        if ly == 0:
            chunk_index = get_chunk_index((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            chunk_index = get_chunk_index((wx, wy + 1, wz))

        if lz == 0:
            chunk_index = get_chunk_index((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            chunk_index = get_chunk_index((wx, wy, wz + 1))

        self.rebuild_chunk(chunk_index)

    def switch_interaction_mode(self):
        self.interaction_mode = not self.interaction_mode

    def update(self):
        self.raycast()

    def raycast(self):
        x1, y1, z1 = self.app.player.position
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_voxel_pos = glm.ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = glm.ivec3(0)
        step_dir = -1

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            result = self.get_voxel_id(voxel_world_pos=current_voxel_pos)
            if result[0]:
                (self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk,) = result
                self.voxel_world_pos = current_voxel_pos

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False

    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH:
            chunk_index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0
