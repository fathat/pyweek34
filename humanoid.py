import pymunk
import math
import utils

class humanoid:
    def __init__(self, base, space):
        self.target = None
        self.space = space

        self.bodyNode = base.loader.loadModel("models/Capsule.stl")
        self.bodyNode.reparentTo(base.render)

        poly = self.makePoly(0.36, 1.74, 10)

        self.body = pymunk.Body(10, 100)
        self.body.position = 50, 30
        shape = pymunk.Poly(self.body, poly)
        shape.friction = 0.5
        shape.filter = pymunk.ShapeFilter(categories=utils.CATEGORY_HUMANOID)
        space.add(self.body, shape)

    def update(self,dt):
        self.body.angle = 0
        self.pos = self.body.position
        rot = self.body.angle
        self.bodyNode.setPos(self.pos.x,0,self.pos.y)
        self.bodyNode.setHpr(0,0,-(rot * 180/3.14))

        if self.target:
            targetPos = self.target.pos
            filter = pymunk.ShapeFilter(mask=utils.CATEGORY_PLAYER)
            result = self.space.point_query_nearest(self.pos, 5, filter)
            
            #if result != None:
                #print(result)
               #print(result[0].point == targetPos)

    def makePoly(self, body_w, body_h, subdivisions):
        body_w = 0.36
        body_h = 1.74
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
