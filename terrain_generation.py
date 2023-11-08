from noise import noise2, noise3
from random import random
from settings import *

@njit
def fractal_noise2(x, y, frequency=2, octaves=8, persistence=0.5, lacunarity=2.0):
    a = 1
    f = frequency
    n = 0
    a_total = 0
    for i in range(octaves):
        a_total += a
        n += noise2(x * f, y * f) * a
        f *= lacunarity
        a *= persistence
    return n/a_total

@njit
def ridge_noise2(x, y, frequency=2, octaves=8, persistence=0.5, lacunarity=2.0):
    return 1-abs(fractal_noise2(x, y, frequency, octaves, persistence, lacunarity))

@njit
def get_height(x, z):
    a1 = WORLD_CENTER_Y

    f1 = 0.005

    height = 0
    ridge_noise_x = ridge_noise2(x, z, frequency=f1)
    ridge_noise_z = ridge_noise2(x+10, z, frequency=f1)
    x += ridge_noise_x * 0.5
    z += ridge_noise_z * 0.5
    height += (fractal_noise2(x, z, frequency=f1, octaves=5)+1) * a1
    return int(height)