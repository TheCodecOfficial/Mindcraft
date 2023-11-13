#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2DArray u_texture_array;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int voxel_id;
flat in int face_dir;

float fog(float dist, float visibility, float density){
    dist -= visibility;
    dist = max(dist, 0);
    return exp(-dist * density)*1;
}

void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_dir, 2) / 3.0;
    vec3 color = texture(u_texture_array, vec3(face_uv, voxel_id)).rgb;
    color = color * shading;
    float dist = gl_FragCoord.z / gl_FragCoord.w;
    //color = mix(vec3(1, 1, 1)*0.9, color, fog(dist, 64, 0.1));

    fragColor = vec4(color, 1);
}