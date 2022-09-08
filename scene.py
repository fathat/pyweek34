from panda3d.core import *
import chopper
import humanoid
import pymunk
from pymunk import Vec2d

import masks
import utils
import distributorOfPain
from scene_colliders import add_node_path_as_collider
from scene_definition import SceneDefinition

pymunk_step = 1.0/120.0


class Scene:
    
    space: pymunk.Space = None
    world: ModelNode
    camera_fov: float = 35

    def __init__(self, app, name):

        self.scene_definition = SceneDefinition(name)
        self.app = app
        self.space = pymunk.Space()
        self.space.gravity = (0.0, self.scene_definition.gravity)
        distributorOfPain.init(self.space)
        self.pymunk_timer = 0.0
        self.camera_fov = 35
        self.cam_dist = -80
       
        color = tuple(self.scene_definition.background_color)
        expfog = Fog("Fog")
        expfog.setExpDensity(self.scene_definition.fog_density)
        expfog.setColor(*color)
        app.setBackgroundColor(*color)

        self.world = app.loader.loadModel(self.scene_definition.world_mesh)
        self.worldNP = NodePath(self.world)
        self.worldNP.reparentTo(self.app.render)
        self.worldNP.setFog(expfog)
        self.worldNP.setShaderAuto()
        
        self.sun = DirectionalLight('Sun')
        self.sun.setColor(LVector3(*tuple(self.scene_definition.sun_color)) * 0.5)
        self.sun.getLens().setFilmSize(400, 200)
        self.sun.getLens().setNearFar(0.1, 500)
        self.sun.setShadowCaster(True, 4096, 4096)
        self.sun.setCameraMask(masks.SUN_SHADOW_CAMERA_MASK)
        self.sunNP = app.render.attachNewNode(self.sun)
        self.sunNP.reparentTo(self.app.render)
        self.sunNP.setPos(0, 0, 500)
        self.sunNP.setHpr(0, -90, 0)
        self.app.render.setLight(self.sunNP)

        print("Shadow buffer size", self.sun.getShadowBufferSize())

        self.extraSun = DirectionalLight('Extra Sun')
        self.extraSun.setColor(LVector3(*tuple(self.scene_definition.sun_color)))   
        self.extraSun.setDirection(LVector3(0.5, 1, -0.5).normalized())
        self.extraSunNP = app.render.attachNewNode(self.extraSun)
        self.extraSunNP.reparentTo(self.app.render)
        self.app.render.setLight(self.extraSunNP)

        self.collisionDebugNP = app.render.attachNewNode("Collision Lines")
        self.collisionDebugNP.hide(masks.SUN_SHADOW_CAMERA_MASK)
        self.collisionDebugNP.clearShader()
        add_node_path_as_collider(self.world, self.worldNP, self.space, self.collisionDebugNP)

        self.chopper = chopper.Chopper(app, self, self.scene_definition.spawn_point)

        #print(app.render.ls())  
        self.npcs = []
        x = -99
        for i in range(0, 10):
            human = humanoid.Humanoid(app, self.space)
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
            
            self.sunNP.setPos(self.chopper.pos.x, 0, self.chopper.pos.y + 250)
            
            cam_dist = -45 * abs(self.chopper.body.velocity_at_local_point((0,0))) / 10
            cam_dist = max(-45, min(cam_dist, -20))

            self.cam_dist = utils.firstorder_lowpass(self.cam_dist, cam_dist, dt, 1.0)

            #self.app.camera.setPos(self.chopper.pos.x, -45, self.chopper.pos.y + 5)
            self.app.camera.setPos(self.chopper.pos.x, self.cam_dist, self.chopper.pos.y + 15)
            self.app.camera.lookAt(self.chopper.pos.x, 0, self.chopper.pos.y)

            # fov_target = 60 + utils.clamp((self.chopper.velocity() / 5.0) * 0.5 + self.chopper.body.angular_velocity.length , 0.0, 1.0) * 25
            # self.camera_fov = utils.move_towards(self.camera_fov, fov_target, 5, dt)

            # self.app.camLens.set_fov(self.camera_fov)
