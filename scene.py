from panda3d.core import *
import chopper
import humanoid
import pymunk
from pymunk import Vec2d
import utils
import distributorOfPain

pymunk_step = 1.0/120.0

class Scene:
    def __init__(self, app):
        self.app = app
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -9.8)
        distributorOfPain.init(self.space)
        self.pymunk_timer = 0.0

        lines = LineSegs()
        lines.setColor(1, 0, 0, 1)
        lines.moveTo(-100, 0, 10)
        lines.drawTo(100, 0, -10)
        lines.setThickness(4)
        node = lines.create()
        np = NodePath(node)
        np.reparentTo(app.render)

        shape = pymunk.Segment(self.space.static_body, Vec2d(-100, 10), Vec2d(100, -10), 0.0)
        shape.friction = 1.0
        shape.filter = pymunk.ShapeFilter(categories=utils.CATEGORY_WALL)
        self.space.add(shape)

        self.chopper = chopper.Chopper(app, self.space)

        self.npcs = []
        x = -99
        for i in range(0, 10):
            human = humanoid.humanoid(app, self.space)
            human.target = self.chopper
            human.setPos(x, 20)
            x += 20
            self.npcs.append(human)

    def update(self, dt):
        self.pymunk_timer += dt

        while self.pymunk_timer >= pymunk_step:
            self.pymunk_timer -= pymunk_step
            self.space.step(pymunk_step)
            self.chopper.update(pymunk_step)

            for i in range(len(self.npcs) - 1, -1, -1):
                if self.npcs[i].destroyed:
                    self.npcs.pop(i)
                else:
                    self.npcs[i].update(pymunk_step)
            
            self.app.camera.setPos(self.chopper.pos.x, -100, self.chopper.pos.y)
