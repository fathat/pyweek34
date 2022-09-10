from direct.showbase.ShowBase import ShowBase
from panda3d.physics import *
from panda3d.core import *
from direct.gui.DirectGui import OnscreenText
from direct.actor import Actor
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from direct.filter.CommonFilters import CommonFilters

import utils
import cutscene
import sys
from scene import Scene
from gltf.loader import GltfLoader
from gltf.converter import GltfSettings

from input import InputManager
import simplepbr

GltfLoader.global_settings = GltfSettings(
    physics_engine='builtin',
    print_scene=True,
    skip_axis_conversion=False,
    no_srgb=True,
    textures='ref',
    legacy_materials=True,
    animations='embed'
)

load_prc_file_data("", """
    show-frame-rate-meter 1
    sync-video 1
    win-size 1600 900
    window-title SPACE CHOPPER!!
    want-pstats 0
    pstats-tasks 0
    task-timer-verbose 0
    want-directtools #f
    want-tk #f
    load-file-type p3assimp
    model-cache-dir
    hardware-animated-vertices true
    basic-shaders-only false
""")

class RedPlanetApp(ShowBase):
    gamepad = None
    scene: Scene = None

    def __init__(self):
        ShowBase.__init__(self)
        self.pushBias = 0.04
        self.font = self.loader.loadFont("art/fonts/bedstead/bedstead.otf")
        
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(self.ambientLightNodePath)
        self.enableParticles()
        self.disableMouse()
        self.input = InputManager(self)
        self.accept("v", base.bufferViewer.toggleEnable)
        self.perPixelEnabled = True
        self.shadowsEnabled = True
        self.camLens.set_fov(90)
        self.camLens.set_near_far(1, 10000)
        self.camera.setPos(0, -50, 0)
        self.script = []
        self.scriptIndex = 0

        script = open("scenes/space_choppa.txt", "r")
        for line in script:
            self.script.append(line.rstrip('\n').split(" "))

        self.progress_story()

        self.render.setShaderInput('push', self.pushBias)
        self.render.setColorOff()

        # materials = self.render.findAllMaterials()
        # for material in materials:
        #     print(material)

        self.altText = OnscreenText(text="Altitude: ?", font=self.font, style=2, fg=(1, 1, 1, 1), bg=(0, 0, 0, 0.5), scale=.05,
                        shadow=(0, 0, 0, 1), parent=self.a2dBottomLeft,
                        pos=(0.05, 0.05), align=TextNode.ALeft)
        self.speedText = OnscreenText(text="Speed: ?", font=self.font, style=2, fg=(1, 1, 1, 1), bg=(0, 0, 0, 0.5), scale=.05,
                        shadow=(0, 0, 0, 1), parent=self.a2dBottomLeft,
                        pos=(0.05, 0.11), align=TextNode.ALeft)

        self.d2gText = OnscreenText(text="D2G: ?", font=self.font, style=2, fg=(1, 1, 1, 1), bg=(0, 0, 0, 0.5), scale=.05,
                        shadow=(0, 0, 0, 1), parent=self.a2dBottomLeft,
                        pos=(0.05, 0.17), align=TextNode.ALeft)
        self.capacityText = OnscreenText(text="Passengers: 0", font=self.font, style=2, fg=(1, 1, 1, 1), bg=(0, 0, 0, 0.5), scale=.05,
                        shadow=(0, 0, 0, 1), parent=self.a2dBottomLeft,
                        pos=(0.05, 0.23), align=TextNode.ALeft)

        #self.worldText = OnscreenText(text="I am world", font=self.font, style=2, fg=(1, 1, 1, 1), bg=(0, 0, 0, 0.5), scale=.05,
        #                shadow=(0, 0, 0, 1), parent=self.aspect2d,
        #                pos=(0.05, 0.23), align=TextNode.ACenter)

        self.clock = ClockObject.getGlobalClock()
        self.updateTask = taskMgr.add(self.update_task, "update_task")


    def update_task(self, task: Task):
        done = self.scene.update(self.clock.dt)

        if self.scene.show_hud:
            #self.scene.update(self.clock.dt)
            self.altText.setText("Altitude: " + str(int(self.scene.chopper.pos.y)) + "m")
            self.speedText.setText(f"Speed: {int(self.scene.chopper.velocity())}")
            self.d2gText.setText(f"Distance To Ground: {int(self.scene.chopper.distance_to_ground)}")
            self.capacityText.setText(f"Passengers: {self.scene.chopper.rescued}/{self.scene.chopper.capacity}")
        if done:
            if not self.progress_story():
                sys.exit() #this feels wrong...

        return Task.cont

    def progress_story(self):
        if self.scene != None:
            self.scene.destroy()

        if self.scriptIndex >= len(self.script):
            return False

        if self.script[self.scriptIndex][0] == "image":
            self.scene = cutscene.CutScene(self, self.script[self.scriptIndex][1])
        elif self.script[self.scriptIndex][0] == "level":
            self.scene = Scene(self, self.script[self.scriptIndex][1])

        self.scriptIndex += 1
        return True

if __name__ == '__main__':
    RedPlanetApp().run()