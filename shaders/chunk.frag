#version 330 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D u_texture_uv_debug;

in vec3 voxel_color;
in vec2 uv;
in float shading;

void main(){
    vec3 color = texture(u_texture_uv_debug, uv).rgb;
    //color = mix(vec3(1, 1, 1), color, 0.001);
    //color = mix(vec3(1, 1, 1), color, 0);
    color = color * shading;
    fragColor = vec4(color, 1);
}