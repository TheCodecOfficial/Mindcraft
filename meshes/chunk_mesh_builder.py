from settings import *


def is_void(voxel_pos, chunk_voxels) -> bool:
    x, y, z = voxel_pos
    if x < 0 or x >= CHUNK_SIZE:
        return True
    if y < 0 or y >= CHUNK_SIZE:
        return True
    if z < 0 or z >= CHUNK_SIZE:
        return True
    return not chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]


def add_data(vertex_data, index, *vertices) -> int:
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index


def build_chunk_mesh(chunk_voxels, format_size):
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype="uint8")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA]
                if not voxel_id:
                    continue

                if is_void((x, y + 1, z), chunk_voxels):
                    index = build_face(0, vertex_data, index, x, y, z, voxel_id)
                if is_void((x, y - 1, z), chunk_voxels):
                    index = build_face(1, vertex_data, index, x, y, z, voxel_id)
                if is_void((x + 1, y, z), chunk_voxels):
                    index = build_face(2, vertex_data, index, x, y, z, voxel_id)
                if is_void((x - 1, y, z), chunk_voxels):
                    index = build_face(3, vertex_data, index, x, y, z, voxel_id)
                if is_void((x, y, z - 1), chunk_voxels):
                    index = build_face(4, vertex_data, index, x, y, z, voxel_id)
                if is_void((x, y, z + 1), chunk_voxels):
                    index = build_face(5, vertex_data, index, x, y, z, voxel_id)

    return vertex_data[:index]


def build_face(face_dir, vertex_data, index, x, y, z, voxel_id):
    if face_dir == 0:  # top face
        v0 = (x, y + 1, z, voxel_id, face_dir)
        v1 = (x + 1, y + 1, z, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x, y + 1, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    if face_dir == 1:  # bottom face
        v0 = (x, y, z + 1, voxel_id, face_dir)
        v1 = (x + 1, y, z + 1, voxel_id, face_dir)
        v2 = (x + 1, y, z, voxel_id, face_dir)
        v3 = (x, y, z, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    if face_dir == 2:  # right face
        v0 = (x + 1, y, z, voxel_id, face_dir)
        v1 = (x + 1, y + 1, z, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x + 1, y, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

    if face_dir == 3:  # left face
        v0 = (x, y, z + 1, voxel_id, face_dir)
        v1 = (x, y + 1, z + 1, voxel_id, face_dir)
        v2 = (x, y + 1, z, voxel_id, face_dir)
        v3 = (x, y, z, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

    if face_dir == 4:  # back face
        v0 = (x, y, z, voxel_id, face_dir)
        v1 = (x + 1, y, z, voxel_id, face_dir)
        v2 = (x + 1, y + 1, z, voxel_id, face_dir)
        v3 = (x, y + 1, z, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    if face_dir == 5:  # front face
        v0 = (x + 1, y, z + 1, voxel_id, face_dir)
        v1 = (x, y, z + 1, voxel_id, face_dir)
        v2 = (x, y + 1, z + 1, voxel_id, face_dir)
        v3 = (x + 1, y + 1, z + 1, voxel_id, face_dir)
        return add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
