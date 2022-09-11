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

class Saucer:
    def __init__(self, scene: "scene.Scene"):
        self.scene = scene
        self.target = None
        self.space = scene.space
        self.destroyed = False
        self.hp = 10
        self.team = 2

        self.state = State.IDLE
        self.bodyNode = Actor("models/Saucer.dae")
        self.bodyNode.reparentTo(scene.root)

        poly = ((-5,-1.25),(5,-1.25),(0,3))

        self.body = pymunk.Body(10, 100)
        self.shape = pymunk.Poly(self.body, poly)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_ENEMY)
        self.shape.collision_type = masks.CATEGORY_ENEMY
        self.shape.data = self
        scene.space.add(self.body, self.shape)

        self.weapon = weapons.AlienMachineGun(scene)

        self.snd = scene.app.loader.loadSfx("sound/177912__medetix__pc-quick-lazer.wav")

    def destroy(self):
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.cleanup()
        self.bodyNode.remove_node()

    def update(self,dt):
        if self.hp > 0:
            dist = self.body.position - self.target.body.position

            if abs(self.body.angle) < math.pi / 2:
                force = self.body.mass * -self.space.gravity.y

                #attempt to stabilze
                left = 0.5 * math.sin(self.body.angle) + 0.5
                right = 1 - left

                mod_left = 1.0
                mod_right = 1.0

                velocity = self.body.velocity_at_local_point((0,0))

                if velocity.y < 0:
                    mod_left = 1.1
                    mod_right = 1.1

                if abs(dist.x) < 50:
                    if dist.y > 10:
                        mod_left = 0.9
                        mod_right = 0.9
                    elif dist.y < -10:
                        mod_left = 1.1
                        mod_right = 1.1

                self.body.apply_force_at_local_point((0, force * right * mod_left), (5,0))
                self.body.apply_force_at_local_point((0, force * left * mod_right), (-5,0))
            else:
                #give up
                pass

            #attack!!
            self.weapon.update(dt)

            #move into range
            if dist.x > 10 and dist.x < 100:
                self.body.apply_force_at_local_point((-50, 0), (5,0))
            elif dist.x < -10 and dist.x > -100:
                self.body.apply_force_at_local_point((50, 0), (5,0))

            #fire!
            if dist.x > 0 and dist.x < 100:
                self.weapon.fire(self, utils.Direction.LEFT)
            elif dist.x < 0 and dist.x > -100:
                self.weapon.fire(self, utils.Direction.RIGHT)


        self.bodyNode.setPos(self.body.position.x, 0, self.body.position.y)
        self.bodyNode.setR(-(utils.radians_to_degrees(self.body.angle)))

    def setPos(self, x, y):
        self.body.position = x, y

    def hurt(self, damage):
        self.hp -= damage
        
        if self.hp < 1:
            #self.destroyed = True
            self.bodyNode.cleanup()
            self.bodyNode.remove_node()
            self.bodyNode= Actor("models/Saucer_Broken.dae")
            self.bodyNode.reparentTo(self.scene.root)
            self.scene.kills += 1
            self.snd.play()