from settings import *


class ShaderProgram:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx
        self.player = app.player

        self.chunk_shader = self.get_program(shader='chunk')
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        self.chunk_shader['m_proj'].write(self.player.m_projection)
        self.chunk_shader['m_model'].write(glm.mat4())
        self.chunk_shader['u_texture_array'] = 1

    def update(self):
        self.chunk_shader['m_view'].write(self.player.m_view)

    def get_program(self, shader):
        return self.ctx.program(
            vertex_shader=open(f'shaders/{shader}.vert', 'r').read(),
            fragment_shader=open(f'shaders/{shader}.frag', 'r').read(),
        )
