import pygame as pg
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, pitch=0, yaw=-90):
        self.app = app
        self.speed = 1
        super().__init__(position, pitch, yaw)

    def update(self):
        self.mouse_control()
        self.keyboard_control()
        super().update()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(-mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(-mouse_dy * MOUSE_SENSITIVITY)

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.speed * self.app.delta_time
        if key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_backward(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_e]:
            self.move_up(vel)
        if key_state[pg.K_q]:
            self.move_down(vel)
        if key_state[pg.K_LSHIFT]:
            self.speed = PLAYER_SPRINT_MULTIPLIER
        else:
            self.speed = 1
