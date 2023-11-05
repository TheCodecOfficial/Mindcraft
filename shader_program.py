from settings import *

class ShaderProgram:
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.ctx
        
        self.quad = self.get_program(shader='quad')
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        pass

    def update(self):
        pass

    def get_program(self, shader):
        return self.ctx.program(
            vertex_shader=open(f'shaders/{shader}.vert', 'r').read(),
            fragment_shader=open(f'shaders/{shader}.frag', 'r').read()
        )