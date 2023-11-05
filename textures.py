import pygame as pg
import moderngl as mgl


class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        self.uv_debug = self.load_texture("stone")

        self.uv_debug.use(0)

    def load_texture(self, filename):
        texture = pg.image.load(f"textures/{filename}.png")
        texture = pg.transform.flip(texture, True, False)
        texture = self.ctx.texture(
            size=texture.get_size(),
            components=4,
            data=pg.image.tostring(texture, "RGBA", False),
        )
        texture.anisotropy = 32
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
