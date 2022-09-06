from panda3d.core import *
import chopper
import humanoid
import pymunk
from pymunk import Vec2d

pymunk_step = 1/60

class scene:
    def __init__(self, base):
        self.base = base
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -45.0)
        self.pymunk_timer = 0.0

        lines = LineSegs()
        lines.setColor(1, 0, 0, 1)
        lines.moveTo(-100, 200, 10)
        lines.drawTo(100, 200, -10)
        lines.setThickness(4)
        node = lines.create()
        np = NodePath(node)
        np.reparentTo(base.render)

        shape = pymunk.Segment(self.space.static_body, Vec2d(-100, 10), Vec2d(100, -10), 0.0)
        shape.friction = 1.0
        self.space.add(shape)

        self.chopper = chopper.Chopper(base, self.space)
        self.human = humanoid.humanoid(base, self.space)

    def update(self, dt):
        self.pymunk_timer += dt

        if self.pymunk_timer >= pymunk_step:
            self.pymunk_timer -= pymunk_step
            self.space.step(pymunk_step)
            self.chopper.update(pymunk_step)
            self.human.update(pymunk_step)
            self.base.camera.setPos(self.chopper.pos.x,0,self.chopper.pos.y)
