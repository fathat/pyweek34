import pymunk
import input

class chopper:
    def __init__(self, base, space):
        scale = 0.1 #todo get rid of this
        self.bodyNode = base.loader.loadModel("models/Body.stl")
        self.bodyNode.setScale(scale, scale, scale)
        self.bodyNode.reparentTo(base.render)

        self.RoterNode = base.loader.loadModel("models/Roter.stl")
        self.RoterNode.reparentTo(self.bodyNode)


        self.body = pymunk.Body(10, 100)
        self.body.position = 0, 30
        #shape = pymunk.Circle(body, 10, (0, 0))
        shape = pymunk.Poly(self.body, [(-50*scale, -27.5*scale), (50*scale, -27.5*scale), (50*scale, 27.5*scale), (-50*scale, 27.5*scale)])
        #shape = pymunk.Poly.create_box(body, (100*scale, 55*scale))
        shape.friction = 0.5
        space.add(self.body, shape)
        pass

    def update(self,dt):
        if input.upPressed:
            self.body.apply_force_at_local_point((0,1000), (0,0))

        if input.leftPressed:
            self.body.apply_force_at_local_point((-1000,0), (0,0))

        if input.rightPressed:
            self.body.apply_force_at_local_point((1000,0), (0,0))


        self.pos = self.body.position
        rot = self.body.angle
        self.bodyNode.setPos(self.pos.x,200,self.pos.y)
        self.bodyNode.setHpr(0,0,-(rot * 180/3.14))

        self.RoterNode.setHpr(self.RoterNode,1800*dt,0,0)
        pass