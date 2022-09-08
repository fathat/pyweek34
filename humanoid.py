import pymunk
import math

import masks
import utils
from panda3d.core import AmbientLight, Vec4, Material
from direct.actor.Actor import Actor
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    RUN_L = auto()
    RUN_R = auto()
    WAVE = auto()

class Humanoid:
    def __init__(self, base, space):
        self.target = None
        self.space = space
        self.destroyed = False

        self.state = State.IDLE
        self.bodyNode = Actor("art/creative-commons/Ultimate Modular Men- Feb 2022/Individual Characters/glTF/Spacesuit.gltf")
        self.bodyNode.reparentTo(base.render)
        self.bodyNode.loop("Idle")

        poly = self.makePoly(0.36, 1.74, 10)

        self.body = pymunk.Body(10, 100)
        self.body.position = 70, 30
        self.shape = pymunk.Poly(self.body, poly)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_HUMANOID)
        self.shape.collision_type = masks.CATEGORY_HUMANOID
        self.shape.data = self
        space.add(self.body, self.shape)

    def destroy(self):
        self.destroyed = True
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.cleanup()
        self.bodyNode.remove_node()

    def update(self,dt):
        self.new_state = State.IDLE
        self.body.angle = 0
        self.pos = self.body.position

        self.bodyNode.setPos(self.pos.x,0,self.pos.y)
        self.bodyNode.setP(0)

        if self.target:
            filter = pymunk.ShapeFilter(mask=masks.CATEGORY_PLAYER)
            result = self.space.point_query_nearest(self.pos, 30, filter)
            
            if result != None:
                diff = result.point - self.pos

                if diff.y < 5 and abs(self.target.body.velocity_at_local_point((0,0))) < 1:
                    force = 100 * diff.normalized()
                    self.body.apply_force_at_local_point((force.x, 0), (0, 0))
                    
                    if force.x > 0:
                        self.new_state = State.RUN_L
                    else:
                        self.new_state = State.RUN_R

            if self.new_state == State.IDLE:
                if self.target.pos.get_distance(self.pos) <= 30:
                    self.new_state = State.WAVE

        if self.new_state != self.state:
            self.state = self.new_state
            if self.state == State.RUN_L:
                self.bodyNode.setH(90)
                self.bodyNode.loop("Run")
            elif self.state == State.RUN_R:
                self.bodyNode.setH(-90)
                self.bodyNode.loop("Run")
            elif self.state == State.WAVE:
                self.bodyNode.loop("Wave")
                self.bodyNode.setH(0)
            else:
                self.bodyNode.loop("Idle")

    def makePoly(self, body_w, body_h, subdivisions):
        body_radius = body_w/2
        shoulder = body_h - body_w/2
        waist = body_w

        poly = [(body_radius, waist), (body_radius, shoulder)]

        step = math.pi / subdivisions
        for i in range(1, subdivisions):
            angle = step * i
            x = body_radius * math.cos(angle)
            y = body_radius * math.sin(angle)

            poly.append((x, y + shoulder))
            
        poly.append((-body_radius, shoulder))
        poly.append((-body_radius, waist))

        for i in range(subdivisions, subdivisions + subdivisions):
            angle = step * i
            x = body_radius * math.cos(angle)
            y = body_radius * math.sin(angle)

            poly.append((x, y + waist))
        
        return poly

    def setPos(self, x, y):
        self.body.position = x, y