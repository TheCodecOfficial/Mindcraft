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
        self.app.shader_program.chunk_shader['m_model'].write(self.m_model)

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
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = cx + x
                wz = cz + z
                #world_height = get_height(wx, wz)
                #world_height = 32 + x
                #local_height = min(world_height - cy, CHUNK_SIZE)

                b = int(fractal_noise2_norm(wx * 0.02, wz * 0.02) * 9) + 0
                for y in range(CHUNK_SIZE):
                    wy = cy + y
                    y_norm = 2*(wy / (CHUNK_SIZE * WORLD_HEIGHT) - 0.5)
                    density = noise_3D(wx * 0.02+3, wy * 0.02+3, wz * 0.02+3, octaves=2) - 2*y_norm
                    b = 0 if density < 0 else b
                    voxels[x + z * CHUNK_SIZE + y * CHUNK_AREA] = b
