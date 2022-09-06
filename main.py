from direct.showbase.ShowBase import ShowBase
from panda3d.physics import *
from panda3d.core import *
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from scene import Scene
from gltf.loader import GltfLoader

import input
import simplepbr

load_prc_file_data("", """
    show-frame-rate-meter 1
    sync-video 1
    win-size 1280 720
    window-title Space Chopper
    want-pstats 0
    pstats-tasks 0
    task-timer-verbose 0
    want-directtools #f
    want-tk #f
""")

class RedPlanetApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0.0, 0.6, 0.8)
        self.gltfLoader = GltfLoader()
        
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(self.ambientLightNodePath)
        self.enableParticles()
        self.disableMouse()
        input.init(self)

        self.perPixelEnabled = True
        self.shadowsEnabled = True
        self.camLens.set_fov(60)
        self.camLens.set_near_far(1, 10000)
        self.camera.setPos(0, -50, 0)
        self.scene = Scene(self, 'debugscene')
        
        ## We need to use setShaderAuto or simplepbr eventually, but setShaderAut
        ## doesn't seem to be working with lights properly for whatever reason..
        #simplepbr.init(enable_shadows=True, enable_fog=True, use_normal_maps=True)
        #self.render.setShaderAuto()
        #self.render.setLight(self.scene.sunNP)
        self.clock = ClockObject.getGlobalClock()
        self.updateTask = taskMgr.add(self.update_task, "update_task")

    def update_task(self, task: Task):
        self.scene.update(self.clock.dt)
        return Task.cont

if __name__ == '__main__':
    RedPlanetApp().run()