from numba import jit
import numpy as np
import glm
import math

# Resolution
WINDOW_RES = glm.vec2(1900, 1000)

# Chunks
CHUNK_SIZE = 64
HALF_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE

# Camera
ASPECT_RATIO = WINDOW_RES.x / WINDOW_RES.y
FOV = 90
V_FOV = glm.radians(FOV)
H_FOV = 2 * math.atan(math.tan(V_FOV / 2) * ASPECT_RATIO)
NEAR = 0.1
FAR = 1000
PITCH_MAX = glm.radians(89.0)

# Player
PLAYER_SPEED = 0.005
PLAYER_SPRINT_MULTIPLIER = 10
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(HALF_CHUNK_SIZE, CHUNK_SIZE, 1.5 * CHUNK_SIZE)
MOUSE_SENSITIVITY = 0.002

# Colors
BG_COLOR = glm.vec3(0.4, 0.76, 1)
