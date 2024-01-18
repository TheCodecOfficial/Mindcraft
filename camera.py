from settings import *
from frustum import Frustum


class Camera:
    def __init__(self, position, pitch=0, yaw=0):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_projection = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4(1)

        self.frustum = Frustum(self)

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, amount):
        self.pitch += amount
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, amount):
        self.yaw -= amount

    def move_left(self, amount):
        self.position -= self.right * amount

    def move_right(self, amount):
        self.position += self.right * amount

    def move_forward(self, amount):
        self.position += self.forward * amount

    def move_backward(self, amount):
        self.position -= self.forward * amount

    def move_up(self, amount):
        self.position += self.up * amount

    def move_down(self, amount):
        self.position -= self.up * amount
