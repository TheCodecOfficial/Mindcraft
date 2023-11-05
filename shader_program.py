from settings import *


class ShaderProgram:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx
        self.player = app.player

        self.chunk = self.get_program(shader="chunk")
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        self.chunk["m_proj"].write(self.player.m_projection)
        self.chunk["m_model"].write(glm.mat4())
        self.chunk["u_texture_uv_debug"] = 0

    def update(self):
        self.chunk["m_view"].write(self.player.m_view)

    def get_program(self, shader):
        return self.ctx.program(
            vertex_shader=open(f"shaders/{shader}.vert", "r").read(),
            fragment_shader=open(f"shaders/{shader}.frag", "r").read(),
        )
