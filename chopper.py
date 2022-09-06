import pymunk
import input
from utils import not_zero


class Chopper:
    def __init__(self, base, space):
        scale = 0.1 #todo get rid of this
        self.bodyNode = base.loader.loadModel("models/Body.stl")
        self.bodyNode.setScale(scale, scale, scale)
        self.bodyNode.reparentTo(base.render)

        self.roterNode = base.loader.loadModel("models/Roter.stl")
        self.roterNode.reparentTo(self.bodyNode)


        self.body = pymunk.Body(10, 100)
        self.body.position = 0, 30
        #shape = pymunk.Circle(body, 10, (0, 0))
        shape = pymunk.Poly(self.body, [(-50*scale, -27.5*scale), (50*scale, -27.5*scale), (50*scale, 27.5*scale), (-50*scale, 27.5*scale)])
        #shape = pymunk.Poly.create_box(body, (100*scale, 55*scale))
        shape.friction = 0.5
        space.add(self.body, shape)

    def update(self, dt: float):
        if not_zero(input.throttle()):
            self.body.apply_force_at_local_point((0, 1000 * input.throttle()), (0, 0))

        if not_zero(input.pitch_axis()):
            d = -1 if input.pitch_axis() < 0 else 1
            self.body.apply_force_at_local_point((0, 50), (25 * -d, 0))

        # FIXME: this isn't really correct, needs to work with dt or we need a fixed frame rate
        self.body.angular_velocity *= 0.95
        self.body.velocity *= 0.99

        self.pos = self.body.position
        rot = self.body.angle
        self.bodyNode.setPos(self.pos.x,200,self.pos.y)
        self.bodyNode.setHpr(0, 0, -(rot * 180/3.14))

        self.roterNode.setHpr(self.roterNode, 1800 * dt, 0, 0)