from terrain_generation import *
import numpy as np

N = 30
values = [noise_3D(x * 0.1, y * 0.1, z * 0.1, octaves=7) for x in range(N) for y in range(N) for z in range(N)]
values = np.array(values)
avg = np.average(values)
min, max = np.min(values), np.max(values)
print(avg, min, max)
