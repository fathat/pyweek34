from direct.showbase.ShowBase import ShowBase
from panda3d.physics import *
from panda3d.core import *
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from scene import Scene
from gltf.loader import GltfLoader

from input import InputManager
import simplepbr

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
""")

class RedPlanetApp(ShowBase):
    gamepad = None
    scene: Scene = None

    def __init__(self):
        ShowBase.__init__(self)

        if not base.win.getGsg().getSupportsBasicShaders():
            self.t = addTitle(
                "Shadow Demo: Video driver reports that shaders are not supported.")
            return
        if not base.win.getGsg().getSupportsDepthTexture():
            self.t = addTitle(
                "Shadow Demo: Video driver reports that depth textures are not supported.")
            return

        self.setBackgroundColor(0.0, 0.6, 0.8)
        self.gltfLoader = GltfLoader()
        
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
        self.scene = Scene(self, 'debugscene')
        
        ## We need to use setShaderAuto or simplepbr eventually, but setShaderAut
        ## doesn't seem to be working with lights properly for whatever reason..
        #simplepbr.init(enable_shadows=True, enable_fog=True, use_normal_maps=True)
        self.render.setShaderAuto()
        materials = self.render.findAllMaterials()
        print(materials)

#        print(self.render.ls())
        #self.render.setLight(self.scene.sunNP)
        self.clock = ClockObject.getGlobalClock()
        self.updateTask = taskMgr.add(self.update_task, "update_task")


    def update_task(self, task: Task):
        self.scene.update(self.clock.dt)
        return Task.cont

if __name__ == '__main__':
    RedPlanetApp().run()