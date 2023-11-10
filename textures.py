import pygame as pg
import moderngl as mgl


class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        self.marker = self.load_texture('marker')
        self.texture_array = self.load_texture('tex_array', True)

        self.marker.use(0)
        self.texture_array.use(1)

    def load_texture(self, filename, is_texture_array=False):
        texture = pg.image.load(f'textures/{filename}.png')
        texture = pg.transform.flip(texture, True, False)

        if is_texture_array:
            num_layers = 3 * texture.get_height() // texture.get_width()
            texture = self.app.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers,),
                components=4,
                data=pg.image.tostring(texture, 'RGBA'),
            )
        else:
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=4,
                data=pg.image.tostring(texture, 'RGBA', False),
            )
        texture.anisotropy = 32
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
