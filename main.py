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
""")

class RedPlanetApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.gltfLoader = GltfLoader()
        #simplepbr.init()
        self.enableParticles()
        self.disableMouse()
        input.init(self)
        self.camera.setPos(0, -50, 0)
        self.scene = Scene(self)
        self.clock = ClockObject.getGlobalClock()
        self.updateTask = taskMgr.add(self.update_task, "update_task")

    def update_task(self, task: Task):
        self.scene.update(self.clock.dt)
        return Task.cont

if __name__ == '__main__':
    RedPlanetApp().run()