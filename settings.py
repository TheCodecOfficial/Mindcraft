from numba import jit
import numpy as np
import glm
import math

# Resolution
WINDOW_RES = glm.vec2(720, 480)


# Colors
BG_COLOR = glm.vec3(0.4, 0.76, 1)