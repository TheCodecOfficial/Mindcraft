import pygame as pg
from camera import Camera
from settings import *


class PlayerFly:
    def __init__(self, app, position=PLAYER_POS, pitch=0, yaw=0):
        self.app = app
        self.speed = 1
        self.voxel_interaction = None
        self.camera = Camera(position, pitch, yaw)

        self.chunk_pos = glm.ivec3(0)
        self.functions_to_call = []

    def update(self):
        #print(self.camera.position)

        self.mouse_control()
        self.keyboard_control()
        self.camera.update()

        newpos = glm.ivec3(self.camera.position) // CHUNK_SIZE
        if newpos != self.chunk_pos:
            self.chunk_pos = newpos
            for f in self.functions_to_call:
                f()

    def handle_events(self, event):
        return
        if not self.voxel_interaction:
            self.voxel_interaction = self.app.scene.world.voxel_interaction
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.voxel_interaction.set_voxel()
            elif event.button == 3:
                self.voxel_interaction.switch_interaction_mode()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.camera.rotate_yaw(-mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.camera.rotate_pitch(-mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.speed * self.app.delta_time
        if key_state[pg.K_w]:
            self.camera.move_forward(vel)
        if key_state[pg.K_s]:
            self.camera.move_backward(vel)
        if key_state[pg.K_a]:
            self.camera.move_left(vel)
        if key_state[pg.K_d]:
            self.camera.move_right(vel)
        if key_state[pg.K_e]:
            self.camera.move_up(vel)
        if key_state[pg.K_q]:
            self.camera.move_down(vel)
        if key_state[pg.K_LSHIFT]:
            self.speed = PLAYER_SPRINT_MULTIPLIER
        else:
            self.speed = 1
