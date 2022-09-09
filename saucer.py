import pymunk
import math

import masks
import utils
import weapons
from panda3d.core import AmbientLight, Vec4, Material
from direct.actor.Actor import Actor
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUN_L = auto()
    RUN_R = auto()
    WAVE = auto()

class Saucer:
    def __init__(self, base, space):
        self.target = None
        self.space = space
        self.destroyed = False

        self.state = State.IDLE
        self.bodyNode = Actor("models/Saucer.stl")
        self.bodyNode.reparentTo(base.render)

        poly = ((-5,-1.25),(5,-1.25),(0,3))

        self.body = pymunk.Body(10, 100)
        self.shape = pymunk.Poly(self.body, poly)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_ENEMY)
        self.shape.collision_type = masks.CATEGORY_ENEMY
        self.shape.data = self
        space.add(self.body, self.shape)

        self.weapon = weapons.AlienMachineGun(base, space)

    def destroy(self):
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.cleanup()
        self.bodyNode.remove_node()

    def update(self,dt):
        if abs(self.body.angle) < math.pi / 2:
            force = self.body.mass * 9.8

            #attempt to stabilze
            left = 0.5 * math.sin(self.body.angle) + 0.5
            right = 1 - left

            #try to prevent sinking
            velocity = self.body.velocity_at_local_point((0,0))

            if velocity.y < 0:
                left *= 1.1
                right *= 1.1

            self.body.apply_force_at_local_point((0, force * right), (5,0))
            self.body.apply_force_at_local_point((0, force * left), (-5,0))
        else:
            #give up
            pass

        #attack!!
        dist = self.body.position - self.target.body.position
        self.weapon.update(dt)

        #move into range
        if dist.x > 10 and dist.x < 100:
            self.body.apply_force_at_local_point((-50, 0), (5,0))
        elif dist.x < -10 and dist.x > -100:
            self.body.apply_force_at_local_point((50, 0), (5,0))

        #fire!
        if dist.x > 0 and dist.x < 100:
            self.weapon.fire(self.body, utils.Direction.LEFT)
        elif dist.x < 0 and dist.x > -100:
            self.weapon.fire(self.body, utils.Direction.RIGHT)


        self.bodyNode.setPos(self.body.position.x, 0, self.body.position.y)
        self.bodyNode.setR(-(utils.radians_to_degrees(self.body.angle)))

    def setPos(self, x, y):
        self.body.position = x, y