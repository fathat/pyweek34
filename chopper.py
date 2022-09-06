import pymunk
import input
from enum import Enum
from utils import not_zero, radians_to_degrees, damp, move_towards

class Direction(Enum):
    LEFT = -1
    RIGHT = 1

class Chopper:
    width: float = 3.0
    height: float = 1.5
    scale: float = 1.0
    direction: Direction = Direction.RIGHT

    def __init__(self, base, space):
        width, height, scale = self.width, self.height, self.scale

        self.heading = -90
        self.pitch = 0.0
        self.bodyNode = base.loader.loadModel("art/space-chopper/space-chopper.glb")
        self.bodyNode.setScale(scale, scale, scale)
        self.bodyNode.reparentTo(base.render)

        #self.roterNode = base.loader.loadModel("models/Roter.stl")
        #self.roterNode.reparentTo(self.bodyNode)

        self.body = pymunk.Body(5, 100)
        self.body.position = 0, 30
        # shape = pymunk.Circle(body, 10, (0, 0))
        shape = pymunk.Poly(self.body, [(-width*scale, -height*scale), (width*scale, -height*scale), (width*scale, height*scale), (-width*scale, height*scale)])
        # shape = pymunk.Poly.create_box(body, (100*scale, 55*scale))
        shape.friction = 0.5
        space.add(self.body, shape)

    def update(self, dt: float):
        if not_zero(input.throttle()):
            self.body.apply_force_at_local_point((0, 200 * input.throttle()), (0, 0))

        if input.is_face_left_pressed():
            self.direction = Direction.LEFT
        elif input.is_face_right_pressed():
            self.direction = Direction.RIGHT

        if not_zero(input.pitch_axis()):
            self.body.apply_force_at_local_point((0, 200 * input.pitch_axis()), (-self.width, 0))
            self.body.apply_force_at_local_point((0, -200 * input.pitch_axis()), (self.width, 0))


        self.body.angular_velocity = damp(self.body.angular_velocity, 0.15, dt)

        self.pos = self.body.position
        rot = self.body.angle
        
        self.bodyNode.setPos(self.pos.x, 0, self.pos.y)

        self.heading = move_towards(self.heading, 90 * -self.direction.value, 360 * 5, dt)
        self.pitch = move_towards(self.pitch, radians_to_degrees(rot) * self.direction.value, 360 * 5, dt)
        self.bodyNode.setHpr(self.heading, self.pitch, 0)
        # if self.direction == Direction.LEFT:
        #     self.bodyNode.setHpr(90, -(radians_to_degrees(rot)), 0)
        # if self.direction == Direction.RIGHT:
        #     self.bodyNode.setHpr(-90, (radians_to_degrees(rot)), 0)
        #self.roterNode.setHpr(self.roterNode, 1800 * dt, 0, 0)