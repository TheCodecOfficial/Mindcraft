#version 330 core

layout (location = 0) in uint packed_vertex_data;
int x, y, z;
int voxel_id;
int face_dir;
int ao;
int flip_id;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 voxel_color;
out vec2 uv;
out float shading;

const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);

const float face_shading[6] = float[6](
    1.0, 0.5, // Top, Bottom
    0.5, 0.8, // Right, Left
    0.5, 0.8  // Front, Back
);

const vec2 uv_coords[4] = vec2[4](
    vec2(0.0, 0.0),
    vec2(0.0, 1.0),
    vec2(1.0, 0.0),
    vec2(1.0, 1.0)
);

const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3, // Even face
    3, 0, 2, 3, 1, 0, // Odd face
    3, 1, 0, 3, 0, 2, // Even flipped face
    1, 2, 3, 1, 0, 2  // Odd flipped face
);

vec3 hash31(float p){
    vec3 p3  = fract(vec3(p) * vec3(.1031, .11369, .13787));
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.xxy + p3.yzz) * p3.zyx);
}

void unpack_data(uint packed_data){
    x = int((packed_data >> 26u) & 63u);
    y = int((packed_data >> 20u) & 63u);
    z = int((packed_data >> 14u) & 63u);
    voxel_id = int((packed_data >> 6u) & 255u);
    face_dir = int((packed_data >> 3u) & 7u);
    ao = int((packed_data >> 1u) & 3u);
    flip_id = int(packed_data & 1u);
}

void main(){
    unpack_data(packed_vertex_data);
    vec3 in_position = vec3(x, y, z);
    int uv_index = gl_VertexID % 6 + ((face_dir & 1) + flip_id * 2) * 6;
    uv = uv_coords[uv_indices[uv_index]];
    voxel_color = hash31(voxel_id);
    shading = face_shading[face_dir] * ao_values[ao];
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}