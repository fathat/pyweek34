import pymunk
import math
import utils

class humanoid:
    def __init__(self, base, space):
        self.target = None
        self.space = space
        self.destroyed = False

        self.bodyNode = base.loader.loadModel("models/Capsule.stl")
        self.bodyNode.reparentTo(base.render)

        poly = self.makePoly(0.36, 1.74, 10)

        self.body = pymunk.Body(10, 100)
        self.body.position = 70, 30
        self.shape = pymunk.Poly(self.body, poly)
        self.shape.friction = 0.5
        self.shape.filter = pymunk.ShapeFilter(categories=utils.CATEGORY_HUMANOID)
        self.shape.collision_type = utils.CATEGORY_HUMANOID
        self.shape.data = self
        space.add(self.body, self.shape)

    def destroy(self):
        self.destroyed = True
        self.shape.data = None
        self.space.remove(self.body, self.shape)
        self.bodyNode.remove_node()

    def update(self,dt):
        self.body.angle = 0
        self.pos = self.body.position

        self.bodyNode.setPos(self.pos.x,0,self.pos.y)
        self.bodyNode.setHpr(0,0,-utils.radians_to_degrees(self.body.angle))

        if self.target:
            filter = pymunk.ShapeFilter(mask=utils.CATEGORY_PLAYER)
            result = self.space.point_query_nearest(self.pos, 25, filter)
            
            if result != None:
                diff = result.point - self.pos

                if diff.y < 5:
                    force = 100 * diff.normalized()
                    self.body.apply_force_at_local_point((force.x, 0), (0, 0))

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