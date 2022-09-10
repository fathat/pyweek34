import pymunk
import math

import masks
import utils
import weapons
from direct.actor.Actor import Actor
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUN_L = auto()
    RUN_R = auto()
    WAVE = auto()

class Convoy:
    def __init__(self, scene: "scene.Scene"):
        self.target = None
        self.space = scene.space
        self.destroyed = False
        self.hp = 10
        self.team = 1
        self.spawn_point = scene.definition.convoy_spawn_point

        self.bodyNode = Actor("models/truck.dae")
        self.bodyNode.reparentTo(scene.root)

        self.body = pymunk.Body(10, 100)
        self.shape = pymunk.Circle(self.body, 6.5/2)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_ENEMY)
        self.shape.collision_type = masks.CATEGORY_ENEMY
        self.shape.data = self
        scene.space.add(self.body, self.shape)

        self.crash_snd = scene.app.loader.loadSfx("sound/521377__jarusca__rocket-launch.mp3")

    def destroy(self):
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.cleanup()
        self.bodyNode.remove_node()

    def update(self,dt):
        dist = self.body.position - self.target.body.position

        if abs(dist) < 40:
            #self.body.apply_force_at_local_point((50, 0), (0,0))
            self.body.apply_force_at_world_point((25, 0), (self.body.position.x,self.body.position.y + 1))

        self.bodyNode.setPos(self.body.position.x, 0, self.body.position.y)
        #self.bodyNode.setR(-(utils.radians_to_degrees(self.body.angle)))

    def setPos(self, x, y):
        self.body.position = x, y

    def reset(self):
        self.body.position = self.spawn_point
        self.body.angle = 0
        self.hp = 10
        self.crash_snd.play()

    def hurt(self, damage):
        self.hp -= damage
        
        if self.hp < 0:
            self.reset()