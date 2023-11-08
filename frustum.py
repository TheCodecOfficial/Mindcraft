from settings import *


class Frustum:
    def __init__(self, camera):
        self.camera = camera

        self.factor_y = 1.0 / math.cos(half_y := V_FOV / 2)
        self.tan_y = math.tan(half_y)

        self.factor_x = 1.0 / math.cos(half_x := H_FOV / 2)
        self.tan_x = math.tan(half_x)

    def is_inside_frustum(self, chunk):
        sphere_vec = chunk.center - self.camera.position
        sz = glm.dot(sphere_vec, self.camera.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        sy = glm.dot(sphere_vec, self.camera.up)
        dist = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-dist <= sy <= dist):
            return False

        sx = glm.dot(sphere_vec, self.camera.right)
        dist = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-dist <= sx <= dist):
            return False

        return True
