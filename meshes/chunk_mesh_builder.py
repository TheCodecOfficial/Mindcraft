from settings import *
from numba import uint8


@njit
def vertex_uint8(x, y, z, voxel_id, face_dir):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_dir)


@njit
def get_chunk_index(voxel_world_pos) -> int:
    wx, wy, wz = voxel_world_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1
    return cx + cz * WORLD_WIDTH + cy * WORLD_AREA


@njit
def is_void(voxel_pos, voxel_world_pos, world_voxels) -> bool:
    chunk_index = get_chunk_index(voxel_world_pos)
    if chunk_index == -1:
        return True
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = voxel_pos
    voxel_index = (
        x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    )

    if chunk_voxels[voxel_index]:
        return False
    return True


@njit
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


@njit
def build_chunk_mesh(
    chunk_voxels, format_size, chunk_position, world_voxels
) -> np.array:
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]
                if not voxel_id:
                    continue

                ci, cj, ck = chunk_position
                wx = x + ci * CHUNK_SIZE
                wy = y + cj * CHUNK_SIZE
                wz = z + ck * CHUNK_SIZE

                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    v0 = vertex_uint8(x, y + 1, z, voxel_id, 0)
                    v1 = vertex_uint8(x + 1, y + 1, z, voxel_id, 0)
                    v2 = vertex_uint8(x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = vertex_uint8(x, y + 1, z + 1, voxel_id, 0)
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = vertex_uint8(x, y, z, voxel_id, 1)
                    v1 = vertex_uint8(x + 1, y, z, voxel_id, 1)
                    v2 = vertex_uint8(x + 1, y, z + 1, voxel_id, 1)
                    v3 = vertex_uint8(x, y, z + 1, voxel_id, 1)
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = vertex_uint8(x + 1, y, z, voxel_id, 2)
                    v1 = vertex_uint8(x + 1, y + 1, z, voxel_id, 2)
                    v2 = vertex_uint8(x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = vertex_uint8(x + 1, y, z + 1, voxel_id, 2)
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v0 = vertex_uint8(x, y, z, voxel_id, 3)
                    v1 = vertex_uint8(x, y + 1, z, voxel_id, 3)
                    v2 = vertex_uint8(x, y + 1, z + 1, voxel_id, 3)
                    v3 = vertex_uint8(x, y, z + 1, voxel_id, 3)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = vertex_uint8(x, y, z, voxel_id, 4)
                    v1 = vertex_uint8(x + 1, y, z, voxel_id, 4)
                    v2 = vertex_uint8(x + 1, y + 1, z, voxel_id, 4)
                    v3 = vertex_uint8(x, y + 1, z, voxel_id, 4)
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = vertex_uint8(x, y, z + 1, voxel_id, 5)
                    v1 = vertex_uint8(x, y + 1, z + 1, voxel_id, 5)
                    v2 = vertex_uint8(x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = vertex_uint8(x + 1, y, z + 1, voxel_id, 5)
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index]
