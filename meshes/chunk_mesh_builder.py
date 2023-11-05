from settings import *


def get_chunk_index(voxel_world_pos) -> int:
    wx, wy, wz = voxel_world_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1
    return cx + cz * WORLD_WIDTH + cy * WORLD_AREA


def is_void(voxel_pos, voxel_world_pos, world_voxels) -> bool:
    chunk_index = get_chunk_index(voxel_world_pos)
    if chunk_index == -1:
        return True
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = voxel_pos
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    if chunk_voxels[voxel_index]:
        return False
    return True


def add_data(vertex_data, index, *vertices) -> int:
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(
    chunk_voxels, format_size, chunk_position, world_voxels
) -> np.array:
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size * 2, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]
                if not voxel_id:
                    continue

                cx, cy, cz = glm.ivec3(chunk_position) * CHUNK_SIZE
                wx = cx + x
                wy = cy + y
                wz = cz + z

                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    index = build_face(0, vertex_data, index, x, y, z, voxel_id)
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    index = build_face(1, vertex_data, index, x, y, z, voxel_id)
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    index = build_face(2, vertex_data, index, x, y, z, voxel_id)
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    index = build_face(3, vertex_data, index, x, y, z, voxel_id)
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    index = build_face(4, vertex_data, index, x, y, z, voxel_id)
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    index = build_face(5, vertex_data, index, x, y, z, voxel_id)

    return vertex_data[:index]


def build_face(face_dir, vertex_data, index, x, y, z, voxel_id) -> int:
    if face_dir == 0:  # top face
        v0 = (x, y + 1, z, voxel_id, face_dir)
        v1 = (x + 1, y + 1, z, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x, y + 1, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

    if face_dir == 1:  # bottom face
        v0 = (x, y, z, voxel_id, face_dir)
        v1 = (x + 1, y, z, voxel_id, face_dir)
        v2 = (x + 1, y, z + 1, voxel_id, face_dir)
        v3 = (x, y, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

    if face_dir == 2:  # right face
        v0 = (x + 1, y, z, voxel_id, face_dir)
        v1 = (x + 1, y + 1, z, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x + 1, y, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

    if face_dir == 3:  # left face
        v0 = (x, y, z, voxel_id, face_dir)
        v1 = (x, y + 1, z, voxel_id, face_dir)
        v2 = (x, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x, y, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    if face_dir == 4:  # back face
        v0 = (x, y, z, voxel_id, face_dir)
        v1 = (x + 1, y, z, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z, voxel_id, face_dir)
        v3 = (x, y + 1, z, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

    if face_dir == 5:  # front face
        v0 = (x, y, z + 1, voxel_id, face_dir)
        v1 = (x, y + 1, z + 1, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x + 1, y, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
