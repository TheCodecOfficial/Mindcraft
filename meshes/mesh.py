import numpy as np


class Mesh:
    def __init__(self):
        # moderngl context
        self.ctx = None
        # shader program
        self.shader = None
        # vertex buffer format
        self.vbo_format = None
        # attributes
        self.attrs: tuple[str, ...] = None
        # vertex array object
        self.vao = None

    def get_vertex_data(self) -> np.array:
        ...

    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.shader, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True
        )
        return vao

    def render(self):
        self.vao.render()
