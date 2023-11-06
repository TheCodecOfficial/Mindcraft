from numba import uint8


def pack_vertex_data(x, y, z, voxel_id, face_dir, ao, flip_id):
    packed = (
        uint8(x) << 26
        | uint8(y) << 20
        | uint8(z) << 14
        | uint8(voxel_id) << 6
        | uint8(face_dir) << 3
        | uint8(ao) << 1
        | uint8(flip_id)
    )
    return packed


def unpack_data(packed):
    x = (packed >> 26) & 0x3F
    y = (packed >> 20) & 0x3F
    z = (packed >> 14) & 0x3F
    voxel_id = (packed >> 6) & 0xFF
    face_dir = (packed >> 3) & 0x7
    ao = (packed >> 1) & 0x3
    flip_id = packed & 0x1
    return x, y, z, voxel_id, face_dir, ao, flip_id


x = 5
y = 0
z = 1
voxel_id = 63
face_dir = 2
ao = 3
flip_id = 1
packed = pack_vertex_data(x, y, z, voxel_id, face_dir, ao, flip_id)
print(packed)
x_, y_, z_, voxel_id_, face_dir_, ao_, flip_id_ = unpack_data(packed)
print(x_, y_, z_, voxel_id_, face_dir_, ao_, flip_id_)
