from panda3d.core import *
import chopper
import humanoid
import pymunk
from pymunk import Vec2d
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
       
        color = tuple(self.scene_definition.background_color)
        expfog = Fog("Fog")
        expfog.setExpDensity(self.scene_definition.fog_density)
        expfog.setColor(*color)
        app.setBackgroundColor(*color)

        self.world = app.loader.loadModel(self.scene_definition.world_mesh)
        self.worldNP = NodePath(self.world)
        self.worldNP.reparentTo(self.app.render)
        self.worldNP.setFog(expfog)
        
        self.sun = DirectionalLight('Sun')
        self.sun.setColor(LVector3(*tuple(self.scene_definition.sun_color)))
        self.sun.setDirection(LVector3(0, 1, -1).normalized())
        self.sun.setShadowCaster(True, 1024, 1024)
        self.sunNP = app.render.attachNewNode(self.sun)
        self.app.render.setLight(self.sunNP)       

        add_node_path_as_collider(self.world, self.worldNP, self.space, app.render)

        self.chopper = chopper.Chopper(app, self)

        print(app.render.ls())  
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
            
            self.app.camera.setPos(self.chopper.pos.x, -80, self.chopper.pos.y + 15)
            self.app.camera.lookAt(self.chopper.pos.x, 0, self.chopper.pos.y)

            # fov_target = 60 + utils.clamp((self.chopper.velocity() / 5.0) * 0.5 + self.chopper.body.angular_velocity.length , 0.0, 1.0) * 25
            # self.camera_fov = utils.move_towards(self.camera_fov, fov_target, 5, dt)

            # self.app.camLens.set_fov(self.camera_fov)
