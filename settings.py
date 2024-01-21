from numba import njit
import numpy as np
import glm
import math

# Resolution
WINDOW_RES = glm.vec2(1920, 1080)

# Raycasting
MAX_RAY_DIST = 10

# Chunks
CHUNK_SIZE = 32
HALF_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = HALF_CHUNK_SIZE * math.sqrt(3)

# World
SEED = 42
WORLD_WIDTH, WORLD_HEIGHT = 64, 16
WORLD_DEPTH = WORLD_WIDTH
WORLD_AREA = WORLD_WIDTH * WORLD_DEPTH
WORLD_VOL = WORLD_AREA * WORLD_HEIGHT
WORLD_CENTER_XZ = WORLD_WIDTH * HALF_CHUNK_SIZE
WORLD_CENTER_Y = WORLD_HEIGHT * HALF_CHUNK_SIZE
RENDER_DISTANCE = 80
GENERATE_DISTANCE = 32

# Camera
ASPECT_RATIO = WINDOW_RES.x / WINDOW_RES.y
FOV = 90
V_FOV = glm.radians(FOV)
H_FOV = 2 * math.atan(math.tan(V_FOV / 2) * ASPECT_RATIO)
NEAR = 0.1
FAR = 1000
PITCH_MAX = glm.radians(89.0)

# Player
PLAYER_SPEED = 4.317
PLAYER_SPRINT_MULTIPLIER = 20
PLAYER_ROT_SPEED = 0.003
PLAYER_HEIGHT = 1.7
PLAYER_POS = glm.vec3(WORLD_CENTER_XZ, 186, WORLD_CENTER_XZ)
PLAYER_HITBOX_RADIUS = 0.25
JUMP_STRENGTH = 8
MOUSE_SENSITIVITY = 0.001

# Physics
GRAVITY = 9.81 * 2

# Colors
BG_COLOR = glm.vec3(0.4, 0.76, 1)
BG_COLOR = glm.vec3(0.6, 0.85, 1)
