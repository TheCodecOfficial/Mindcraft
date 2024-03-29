from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from playerfly import PlayerFly
from textures import Textures
from world_util import WorldUtil
import ctypes

ctypes.windll.user32.SetProcessDPIAware()


class Engine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        pg.display.set_mode(WINDOW_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = "auto"

        # self.fbo = self.ctx.framebuffer()

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        self.slow_time = 0

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.is_running = True
        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = PlayerFly(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        self.world_util = WorldUtil(self)
        self.player.world_util = self.world_util

    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        # self.delta_time = self.clock.tick() * 0.001
        self.clock.tick(240)
        fps = self.clock.get_fps()
        if fps > 0:
            self.delta_time = 1.0 / self.clock.get_fps()
        else:
            self.delta_time = 0
        self.time = pg.time.get_ticks() * 0.001
        self.slow_time += self.delta_time
        if self.slow_time > 1:
            self.slow_time -= 1
            self.slow_tick()
        pg.display.set_caption(f"FPS: {fps :.0f}")

    def slow_tick(self):
        self.scene.world.cleanup_chunks()

    def render(self):
        self.ctx.clear(color=BG_COLOR)

        self.scene.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            self.player.handle_events(event)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    app = Engine()
    app.run()
