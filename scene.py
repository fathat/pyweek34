import random

from panda3d.core import *
import chopper
import humanoid
import saucer
import pymunk
from pymunk import Vec2d

import masks
import utils
import distributorOfPain
from scene_colliders import add_node_path_as_collider
from scene_definition import SceneDefinition

pymunk_step = 1.0/120.0


class Scene:
    root: NodePath = None
    space: pymunk.Space = None
    world: ModelNode
    camera_fov: float = 35
    num_rescued: int = 0

    def __init__(self, app, name):
        self.definition = SceneDefinition(name)
        self.root = NodePath("Scene Root")
        self.root.reparentTo(app.render)
        self.app = app
        self.space = pymunk.Space()
        self.space.gravity = (0.0, self.definition.gravity)
        distributorOfPain.init(self.space)
        self.pymunk_timer = 0.0
        self.camera_fov = 35
        self.cam_dist = -80
        self.show_hud = True
       
        color = tuple(self.definition.background_color)
        expfog = Fog("Fog")
        expfog.setExpDensity(self.definition.fog_density)
        expfog.setColor(*color)
        app.setBackgroundColor(*color)

        self.world = app.loader.loadModel(self.definition.world_mesh)
        self.worldNP = NodePath(self.world)
        self.worldNP.reparentTo(self.root)
        self.worldNP.setFog(expfog)
        self.worldNP.setShaderAuto()
        self.worldNP.setColorOff()

        if self.definition.texture_hack:
            self.worldNP.setTextureOff(1)

        # need to set a depth offset or we get shadow acne
        self.worldNP.setDepthOffset(-2)
        
        self.sun = DirectionalLight('Sun')
        self.sun.setColor(LVector3(*tuple(self.definition.sun_color)) * 0.5)
        self.sun.getLens().setFilmSize(400, 200)
        self.sun.getLens().setNearFar(1, 400)
        self.sun.setShadowCaster(True, 2048, 2048)
        self.sun.setCameraMask(masks.SUN_SHADOW_CAMERA_MASK)
        self.sunNP = app.render.attachNewNode(self.sun)
        self.sunNP.reparentTo(self.app.render)
        self.sunNP.setPos(0, 0, 500)
        self.sunNP.setHpr(0, -90, 0)
        self.root.setLight(self.sunNP)

        print("Shadow buffer size", self.sun.getShadowBufferSize())

        self.extraSun = DirectionalLight('Extra Sun')
        self.extraSun.setColor(LVector3(*tuple(self.definition.sun_color)))
        self.extraSun.setDirection(LVector3(0.5, 1, -0.5).normalized())
        self.extraSunNP = app.render.attachNewNode(self.extraSun)
        self.extraSunNP.reparentTo(self.root)
        self.root.setLight(self.extraSunNP)

        # self.testNP = self.root.attachNewNode(TextNode("Cool Path Bro"))
        # self.testNP.node().text = "Cool Path Bruh"
        # self.testNP.node().setTextScale(2)
        # self.testNP.node().setTextColor(LVector4f(1.0, 0.0, 0.0, 1.0))
        # self.testNP.node().setShadowColor(LVector4f(0.0, 0.0, 0.0, 1.0))
        # self.testNP.setPos(25, 5, 20)

        self.collisionDebugNP = self.root.attachNewNode("Collision Lines")
        self.collisionDebugNP.hide(masks.SUN_SHADOW_CAMERA_MASK)
        self.collisionDebugNP.clearShader()
        add_node_path_as_collider(self.world, self.worldNP, self.space, self.collisionDebugNP)
        #add_node_path_as_collider(self.world, self.worldNP, self.space, None)

        self.chopper = chopper.Chopper(self, self.definition.spawn_point)

        self.objects = []
        self.fires = []

        enemy = saucer.Saucer(self)
        self.objects.append(enemy)
        enemy.setPos(self.definition.spawn_point[0] + 50, self.definition.spawn_point[1] + 20)
        enemy.target = self.chopper

        if self.definition.objective == "rescue":
            for i in range(self.definition.num_civilians):
                human = humanoid.Humanoid(self)
                human.target = self.chopper
                x = random.random() * 1000 - 500
                y = self.get_height_at(x) + 2
                human.setPos(x, y)
                self.objects.append(human)

        print(self.root.ls())

    def get_height_at(self, x):
        segment_query_info_list = self.space.segment_query((x, 1000), (x, -2000), 0.1, pymunk.ShapeFilter(mask=masks.CATEGORY_WALL))
        segment_query_info_list.sort(key=lambda x: x.alpha)
        if len(segment_query_info_list) == 0: return -1
        if utils.almost_zero(segment_query_info_list[0].alpha):
            return 0
        return segment_query_info_list[0].point.y

    def update(self, dt):
        self.pymunk_timer += dt

        while self.pymunk_timer >= pymunk_step:
            self.pymunk_timer -= pymunk_step
            self.space.step(pymunk_step)
            self.chopper.update(pymunk_step)

            for i in range(len(self.objects) - 1, -1, -1):
                if self.objects[i].destroyed:
                    self.objects[i].destroy()
                    self.objects.pop(i)
                else:
                    self.objects[i].update(pymunk_step)
            
            self.sunNP.setPos(self.chopper.pos.x, 0, self.chopper.pos.y + 250)

            if self.chopper.distance_to_ground < 5:
                cam_dist = -45 * abs(self.chopper.body.velocity_at_local_point((0,0))) / 10
                cam_dist = max(-45, min(cam_dist, -20))
            else:
                cam_dist = -45

            self.cam_dist = utils.firstorder_lowpass(self.cam_dist, cam_dist, dt, 1.0)
            #self.app.camera.setPos(self.chopper.pos.x, -45, self.chopper.pos.y + 5)
            self.app.camera.setPos(self.chopper.pos.x, self.cam_dist, self.chopper.pos.y + 15)
            self.app.camera.lookAt(self.chopper.pos.x, 0, self.chopper.pos.y)

            # fov_target = 60 + utils.clamp((self.chopper.velocity() / 5.0) * 0.5 + self.chopper.body.angular_velocity.length , 0.0, 1.0) * 25
            # self.camera_fov = utils.move_towards(self.camera_fov, fov_target, 5, dt)

            # self.app.camLens.set_fov(self.camera_fov)

        if self.definition.objective == "rescue":
            if self.chopper.rescued >= self.definition.objective_amount:
                return True

        return False

    def destroy(self):
        self.root.remove_node()

        for i in range(len(self.objects) - 1, -1, -1):
            self.objects[i].destroy()
            self.objects.pop(i)

        self.chopper.destroy()
        self.space = None #how the hell do I clean this up?