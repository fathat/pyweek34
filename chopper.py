from panda3d.core import PointLight, LVector3, LensNode, PerspectiveLens, SamplerState, TextureStage
import pymunk
from input import InputManager
from enum import Enum
from utils import not_zero, radians_to_degrees, damp, move_towards, CATEGORY_PLAYER


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


class Chopper:
    width: float = 3.0
    height: float = 1.5
    scale: float = 1.0
    direction: Direction = Direction.RIGHT

    def __init__(self, app, scene):
        width, height, scale = self.width, self.height, self.scale
        space = scene.space
        self.input = app.input
        self.score = 0
        self.heading = -90
        self.pitch = 0.0
        self.bodyNode = app.loader.loadModel("art/space-chopper/space-chopper.glb")
        self.bodyNode.setScale(scale, scale, scale)
        self.bodyNode.reparentTo(app.render)

        # self.shadowNode = self.bodyNode.attachNewNode(LensNode('shadowproj'))
        # #lens = PerspectiveLens()
        # lens = PerspectiveLens()
        # lens.setNearFar(1, 5)
        # self.shadowNode.node().setLens(lens)
        # self.shadowNode.node().showFrustum()
        # self.shadowNode.setHpr(0, -90, 0)
        # self.shadowNode.find('frustum').setColor(1, 0, 0, 1)
        # self.shadowNode.reparentTo(self.bodyNode)
        # self.shadowNode.setPos(0, 0, self.height)

        # tex = app.loader.loadTexture('art/space-chopper/shadow.png')
        # tex.setWrapU(SamplerState.WMBorderColor)
        # tex.setWrapV(SamplerState.WMBorderColor)
        # tex.setBorderColor((1, 1, 1, 0))
        # ts = TextureStage('ts')
        # ts.setSort(1)
        # ts.setColor((0.5, 0.5, 0.5, 0.5))
        # ts.setMode(TextureStage.MCombine)
        # ts.setCombineRgb(
        #     TextureStage.CMInterpolate, 
        #     TextureStage.CSTexture, 
        #     TextureStage.COSrcColor,
        #     TextureStage.CSPrevious,
        #     TextureStage.COSrcColor,
        #     TextureStage.CSTexture,
        #     TextureStage.COOneMinusSrcColor
        #     )
        # scene.worldNP.projectTexture(ts, tex, self.shadowNode)

        self.light = PointLight("ChopperLight")
        self.light.setAttenuation(LVector3(1, 0, 1))
        self.light.setMaxDistance(60)
        self.lightNP = self.bodyNode.attachNewNode(self.light)
        self.lightNP.reparentTo(self.bodyNode)
        
        app.render.setLight(self.lightNP)
        

        #self.roterNode = base.loader.loadModel("models/Roter.stl")
        #self.roterNode.reparentTo(self.bodyNode)

        self.body = pymunk.Body(5, 100)
        self.body.position = 0, 30
        shape = pymunk.Poly(self.body, [(-width*scale, -height*scale), (width*scale, -height*scale), (width*scale, height*scale), (-width*scale, height*scale)])
        shape.friction = 0.5
        shape.filter = pymunk.ShapeFilter(categories=CATEGORY_PLAYER)
        shape.collision_type = CATEGORY_PLAYER
        shape.data = self
        space.add(self.body, shape)

    def velocity(self) -> float: return self.body.velocity.length

    def update(self, dt: float):
        input: InputManager = self.input

        if not_zero(input.throttle()):
            self.body.apply_force_at_local_point((0, 200 * input.throttle()), (0, 0))

        if input.is_booster_rocket_pressed():
            self.body.apply_force_at_local_point((self.direction.value * 200, 0), (0, 0))
        
        if input.is_reverse_booster_rocket_pressed():
            self.body.apply_force_at_local_point((-self.direction.value * 200, 0), (0, 0))

        if input.is_face_left_pressed():
            self.direction = Direction.LEFT
        elif input.is_face_right_pressed():
            self.direction = Direction.RIGHT

        if not_zero(input.pitch_axis()):
            self.body.apply_force_at_world_point((10 * input.pitch_axis(), 0), (self.body.position.x, self.body.position.y))
            self.body.apply_force_at_local_point((0, 200 * input.pitch_axis()), (-self.width, 0))
            self.body.apply_force_at_local_point((0, -200 * input.pitch_axis()), (self.width, 0))


        self.body.velocity = damp(self.body.velocity, .95, dt)
        self.body.angular_velocity = damp(self.body.angular_velocity, 0.15, dt)
                

        self.pos = self.body.position
        rot = self.body.angle
        
        self.bodyNode.setPos(self.pos.x, 0, self.pos.y)
        # self.shadowNode.setHpr(0, -radians_to_degrees(rot) - 90, 0)

        self.heading = move_towards(self.heading, 90 * -self.direction.value, 360 * 5, dt)
        self.pitch = move_towards(self.pitch, radians_to_degrees(rot) * self.direction.value, 360 * 5, dt)
        self.bodyNode.setHpr(self.heading, self.pitch, 0)

    def pickup(self, human):
        human.destroy()
        self.score += 1