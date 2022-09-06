from direct.showbase.ShowBase import ShowBase
from panda3d.physics import *
from panda3d.core import *
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
import scene
import input

load_prc_file_data("", """
    show-frame-rate-meter 1
    sync-video 1
""")

class RedPlanetApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.enableParticles()
        self.disableMouse()
        input.init(self)
        self.scene = scene.scene(self)
        self.clock = ClockObject.getGlobalClock()
        self.updateTask = taskMgr.add(self.update_task, "update_task")

    def update_task(self, task: Task):
        if self.clock.dt > 1.0/59.0:
            print(self.clock.dt, 1.0/60.0)
        self.scene.update(1.0/60.0)
        return Task.cont

if __name__ == '__main__':
    RedPlanetApp().run()