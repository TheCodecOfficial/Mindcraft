#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D u_texture_uv_debug;

in vec3 voxel_color;
in vec2 uv;

void main(){
    vec3 color = texture(u_texture_uv_debug, uv).rgb;
    fragColor = vec4(color, 1);
}