import pygame as pg
from camera import Camera
from settings import *


class Player:
    def __init__(self, app, position=PLAYER_POS, pitch=0, yaw=0):
        self.app = app
        self.world_util = None
        self.voxel_interaction = None
        self.camera = Camera(position, pitch, yaw)

        self.speed = 1
        self.grounded = True
        self.position = position
        self.velocity = glm.vec3(0, 0, 0)
        self.acceleration = glm.vec3(0, 0, 0)
        self.max_speed = PLAYER_SPEED

    def update(self):
        self.mouse_control()
        self.keyboard_control()
        self.physics_update()

        self.camera.update()

    def physics_update(self):
        self.ground_check()
        drag = 0.8 if self.grounded else 0.8
        drag = 1 - 0.5 ** (drag * self.app.delta_time * 200)
        if not self.grounded:
            self.velocity.y -= GRAVITY * self.app.delta_time
        elif self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity += self.acceleration * self.app.delta_time

        magnitude = glm.length(glm.vec2(self.velocity.x, self.velocity.z))
        if drag != 0:
            adjusted_speed = self.max_speed / drag
        else:
            adjusted_speed = self.max_speed
        if magnitude > adjusted_speed:
            self.velocity.x = self.velocity.x / magnitude * adjusted_speed
            self.velocity.z = self.velocity.z / magnitude * adjusted_speed
        self.handle_collisions()

        self.position += self.velocity * self.app.delta_time
        self.camera.position = self.position

        """hypergrounded = self.world_util.is_occupied(
            self.position.x,
            self.position.y - PLAYER_HEIGHT - 0.5,
            self.position.z,
        )
        if hypergrounded:
            self.position.y += 0.005"""

        print(f"Player Y position: {self.position.y}")

        self.acceleration = glm.vec3(0, 0, 0)
        self.velocity.x *= drag
        self.velocity.z *= drag

        # print(f"Velocity: {glm.length(self.velocity)}")

    def handle_collisions(self):
        collision_radius = PLAYER_HITBOX_RADIUS * 2
        height_epsilon = 0.7
        voxel_px_0 = self.world_util.is_occupied(
            self.position.x + collision_radius,
            self.position.y - PLAYER_HEIGHT + 1 - height_epsilon,
            self.position.z,
        )
        voxel_px_1 = self.world_util.is_occupied(
            self.position.x + collision_radius,
            self.position.y - PLAYER_HEIGHT + 2 - height_epsilon,
            self.position.z,
        )
        voxel_nx_0 = self.world_util.is_occupied(
            self.position.x - collision_radius,
            self.position.y - PLAYER_HEIGHT + 1 - height_epsilon,
            self.position.z,
        )
        voxel_nx_1 = self.world_util.is_occupied(
            self.position.x - collision_radius,
            self.position.y - PLAYER_HEIGHT + 2 - height_epsilon,
            self.position.z,
        )
        voxel_pz_0 = self.world_util.is_occupied(
            self.position.x,
            self.position.y - PLAYER_HEIGHT + 1 - height_epsilon,
            self.position.z + collision_radius,
        )
        voxel_pz_1 = self.world_util.is_occupied(
            self.position.x,
            self.position.y - PLAYER_HEIGHT + 2 - height_epsilon,
            self.position.z + collision_radius,
        )
        voxel_nz_0 = self.world_util.is_occupied(
            self.position.x,
            self.position.y - PLAYER_HEIGHT + 1 - height_epsilon,
            self.position.z - collision_radius,
        )
        voxel_nz_1 = self.world_util.is_occupied(
            self.position.x,
            self.position.y - PLAYER_HEIGHT + 2 - height_epsilon,
            self.position.z - collision_radius,
        )

        if (voxel_px_0 or voxel_px_1) and self.velocity.x > 0:
            self.velocity.x = 0
        if (voxel_nx_0 or voxel_nx_1) and self.velocity.x < 0:
            self.velocity.x = 0
        if (voxel_pz_0 or voxel_pz_1) and self.velocity.z > 0:
            self.velocity.z = 0
        if (voxel_nz_0 or voxel_nz_1) and self.velocity.z < 0:
            self.velocity.z = 0

    def ground_check(self):
        bottom_voxel_0 = self.world_util.is_occupied(
            self.position.x - PLAYER_HITBOX_RADIUS,
            self.position.y - PLAYER_HEIGHT,
            self.position.z - PLAYER_HITBOX_RADIUS,
        )
        bottom_voxel_1 = self.world_util.is_occupied(
            self.position.x + PLAYER_HITBOX_RADIUS,
            self.position.y - PLAYER_HEIGHT,
            self.position.z - PLAYER_HITBOX_RADIUS,
        )
        bottom_voxel_2 = self.world_util.is_occupied(
            self.position.x + PLAYER_HITBOX_RADIUS,
            self.position.y - PLAYER_HEIGHT,
            self.position.z + PLAYER_HITBOX_RADIUS,
        )
        bottom_voxel_3 = self.world_util.is_occupied(
            self.position.x - PLAYER_HITBOX_RADIUS,
            self.position.y - PLAYER_HEIGHT,
            self.position.z + PLAYER_HITBOX_RADIUS,
        )
        self.grounded = (
            bottom_voxel_0 or bottom_voxel_1 or bottom_voxel_2 or bottom_voxel_3
        )

    def move(self, direction):
        air_multiplier = 0.75 if not self.grounded else 1
        # air_multiplier = 1
        forward = glm.vec3(glm.cos(self.camera.yaw), 0, glm.sin(self.camera.yaw))
        speed = 100 * air_multiplier
        if direction == "forward":
            self.acceleration += forward * speed
        elif direction == "backward":
            self.acceleration += -forward * speed
        elif direction == "left":
            left = glm.vec3(forward.z, 0, -forward.x)
            self.acceleration += left * speed
        elif direction == "right":
            left = glm.vec3(forward.z, 0, -forward.x)
            self.acceleration += -left * speed

    def jump(self):
        if self.grounded:
            self.velocity.y = JUMP_STRENGTH

    def handle_events(self, event):
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
        if key_state[pg.K_w]:
            self.move("forward")
        if key_state[pg.K_a]:
            self.move("left")
        if key_state[pg.K_s]:
            self.move("backward")
        if key_state[pg.K_d]:
            self.move("right")
        if key_state[pg.K_SPACE]:
            self.jump()
        if key_state[pg.K_LSHIFT]:
            self.max_speed = PLAYER_SPEED * PLAYER_SPRINT_MULTIPLIER
        else:
            self.max_speed = PLAYER_SPEED
