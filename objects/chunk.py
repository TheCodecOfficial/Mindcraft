from settings import *
from meshes.chunk_mesh import ChunkMesh
from terrain_generation import *
import random


class Chunk:
    def __init__(self, world, position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_inside_frustum = self.app.player.camera.frustum.is_inside_frustum

        self.build_voxels()

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniforms(self):
        self.app.shader_program.chunk_shader["m_model"].write(self.m_model)
        self.app.shader_program.chunk_shader["fog_color"].write(BG_COLOR)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_inside_frustum(self):
            self.set_uniforms()
            self.mesh.render()

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOL, dtype=np.uint8)

        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        self.generate_terrain(voxels, cx, cy, cz)

        if np.any(voxels):
            self.is_empty = False

        self.voxels = voxels
        return voxels

    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        r = random.randint(1, 5)
        air_level = 256  # Level at which only air is generated
        for x in range(CHUNK_SIZE):
            wx = cx + x
            for z in range(CHUNK_SIZE):
                wz = cz + z
                if cy > air_level:
                    for y in range(CHUNK_SIZE):
                        wy = cy + y
                        voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = 0
                else:
                    for y in range(CHUNK_SIZE):
                        wy = cy + y
                        y_norm = remap(wy, 0, air_level, -1, 1, clamp=True)

                        density = noise_3D(wx * 0.004, wy * 0.004, wz * 0.004, octaves=5)
                        large_noise = noise_3D(wx * 0.004, wy * 0.004, wz * 0.004, octaves=5)
                        small_noise = noise_3D(wx * 0.01, wy * 0.01, wz * 0.01, octaves=4)
                        flatness = noise_3D(wx * 0.002, wy * 0.002, wz * 0.002, octaves=2, seed=123)
                        flatness = remap(flatness, 0.4, 0.6, 0, 1, clamp=True)
                        flatness = remap(flatness, 0, 1, 1, 20, clamp=True)

                        granularity = noise_3D(wx * 0.0002, wy * 0.0002, wz * 0.0002, octaves=2, seed=345)
                        granularity = remap(granularity, 0.4, 0.6, 0, 1, clamp=True)
                        noise = lerp(large_noise, small_noise, granularity)

                        density = noise - y_norm * flatness

                        humidity = noise_3D(wx * 0.002, 0, wz * 0.002, octaves=8, seed=456)
                        humidity = round(humidity)
                        b = humidity + 1
                        if flatness < 2:
                            b = 4

                        # b = 4
                        b = 0 if density < 0 else b

                        voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = b
