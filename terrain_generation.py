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
    return n / a_total


@njit
def fractal_noise2_norm(x, y, frequency=2, octaves=8, persistence=0.5, lacunarity=2.0):
    return (fractal_noise2(x, y, frequency, octaves, persistence, lacunarity) + 1) / 2


@njit
def ridge_noise2(x, y, frequency=2, octaves=8, persistence=0.5, lacunarity=2.0):
    return 1 - abs(fractal_noise2(x, y, frequency, octaves, persistence, lacunarity))


@njit
def noise_3D(x, y, z, frequency=2, octaves=8, persistence=0.5, lacunarity=2.0):
    a = 1
    f = frequency
    n = 0
    a_total = 0
    for i in range(octaves):
        a_total += a
        n += noise3(x * f, y * f, z * f) * a
        f *= lacunarity
        a *= persistence
    return n / a_total

@njit
def get_height(x, z):
    a1 = WORLD_CENTER_Y

    f1 = 0.0025

    height = 0
    ridge_noise_x = ridge_noise2(x+5.5, z, frequency=f1/2)
    ridge_noise_z = ridge_noise2(x+6.6, z, frequency=f1/2)
    x += ridge_noise_x * 0.5
    z += ridge_noise_z * 0.5
    h = fractal_noise2_norm(x, z, frequency=f1, octaves=6) - 0.15*ridge_noise2(x, z, frequency=f1)**32
    #h = ridge_noise2(x, z, frequency=f1)**32
    #height += h * 384 + 128
    height += h * 64 + 32
    # height += (noise2(x, z)+1)/2 * 384 + 128
    return int(height)
