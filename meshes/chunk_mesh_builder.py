from settings import *
from numba import uint8


@njit
def get_ao(local_pos, world_pos, world_voxels, plane):
    x, y, z = local_pos
    wx, wy, wz = world_pos

    if plane == "Y":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)

    elif plane == "X":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)

    else:  # Z plane
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao


@njit
def vertex_uint8(x, y, z, voxel_id, face_dir, ao, flip_id):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_dir), uint8(ao), uint8(flip_id)


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

                # Top Face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, "Y")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = vertex_uint8(x, y + 1, z, voxel_id, 0, ao[0], flip_id)
                    v1 = vertex_uint8(x + 1, y + 1, z, voxel_id, 0, ao[1], flip_id)
                    v2 = vertex_uint8(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flip_id)
                    v3 = vertex_uint8(x, y + 1, z + 1, voxel_id, 0, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom Face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, "Y")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = vertex_uint8(x, y, z, voxel_id, 1, ao[0], flip_id)
                    v1 = vertex_uint8(x + 1, y, z, voxel_id, 1, ao[1], flip_id)
                    v2 = vertex_uint8(x + 1, y, z + 1, voxel_id, 1, ao[2], flip_id)
                    v3 = vertex_uint8(x, y, z + 1, voxel_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right Face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, "X")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = vertex_uint8(x + 1, y, z, voxel_id, 2, ao[0], flip_id)
                    v1 = vertex_uint8(x + 1, y + 1, z, voxel_id, 2, ao[1], flip_id)
                    v2 = vertex_uint8(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                    v3 = vertex_uint8(x + 1, y, z + 1, voxel_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left Face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, "X")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = vertex_uint8(x, y, z, voxel_id, 3, ao[0], flip_id)
                    v1 = vertex_uint8(x, y + 1, z, voxel_id, 3, ao[1], flip_id)
                    v2 = vertex_uint8(x, y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                    v3 = vertex_uint8(x, y, z + 1, voxel_id, 3, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back Face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, "Z")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = vertex_uint8(x, y, z, voxel_id, 4, ao[0], flip_id)
                    v1 = vertex_uint8(x, y + 1, z, voxel_id, 4, ao[1], flip_id)
                    v2 = vertex_uint8(x + 1, y + 1, z, voxel_id, 4, ao[2], flip_id)
                    v3 = vertex_uint8(x + 1, y, z, voxel_id, 4, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front Face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, "Z")
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = vertex_uint8(x, y, z + 1, voxel_id, 5, ao[0], flip_id)
                    v1 = vertex_uint8(x, y + 1, z + 1, voxel_id, 5, ao[1], flip_id)
                    v2 = vertex_uint8(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flip_id)
                    v3 = vertex_uint8(x + 1, y, z + 1, voxel_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index]
