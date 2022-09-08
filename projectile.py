import pymunk
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import Filename

import masks
import utils

class Missile:
    def __init__(self, app, space, modelfile, pos, angle, force):
        self.space = space
        self.destroyed = False
        self.app = app

        self.bodyNode = app.loader.loadModel(modelfile)
        self.bodyNode.reparentTo(app.render)

        self.body = pymunk.Body(10, 100)
        self.body.position = pos
        self.body.angle = angle

        poly = [(0,-0.4755), (1.35,-0.4755), (1.35,0.4755), (0,0.4755)]
        self.shape = pymunk.Poly(self.body, poly)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_PROJECTILE)
        self.shape.collision_type = masks.CATEGORY_PROJECTILE
        self.shape.data = self
        space.add(self.body, self.shape)

        self.body.apply_impulse_at_local_point((force, 0), (0, 0))

    def update(self, dt: float):
        self.bodyNode.setPos(self.body.position.x, 0, self.body.position.y)
        self.bodyNode.setR(-(utils.radians_to_degrees(self.body.angle)))

    def destroy(self):
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.remove_node()

    def collision(self, other):
        self.destroyed = True
        self.app.scene.fires.append(Fire(self.app.scene, "./art/effects/fireish.ptf", self.body.position))
        #todo hurt other


class Fire:
    def __init__(self, scene, particle_file, pos):
        self.fire_particles = ParticleEffect()
        self.fire_particles.loadConfig(Filename(particle_file))
        self.fire_particles.clearLight()
        self.fire_particles.start(scene.app.render)
        self.fire_particles.setPos(pos.x, 0.000, pos.y)


class Bullet:
    def __init__(self, app, space, modelfile, pos, angle, force):
        self.space = space
        self.destroyed = False

        self.bodyNode = app.loader.loadModel(modelfile)
        self.bodyNode.reparentTo(app.render)

        self.body = pymunk.Body(10, 100)
        self.body.position = pos
        self.body.angle = angle

        self.shape = pymunk.Circle(self.body, 1)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_PROJECTILE)
        self.shape.collision_type = masks.CATEGORY_PROJECTILE
        self.shape.data = self
        space.add(self.body, self.shape)

        self.body.apply_impulse_at_local_point((force, 0), (0, 0))

    def update(self, dt: float):
        self.bodyNode.setPos(self.body.position.x, 0, self.body.position.y)
        #self.bodyNode.setR(-(utils.radians_to_degrees(self.body.angle)))

    def destroy(self):
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.remove_node()

    def collision(self, other):
        self.destroyed = True
        #todo hurt other