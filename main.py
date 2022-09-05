from direct.showbase.ShowBase import ShowBase
from panda3d.physics import *
from panda3d.core import *
import scene
import input


import pymunk
import pymunk.util
from pymunk import Vec2d

#x = left/right
#y = fwd/back
#z = up/down

base = ShowBase()
base.enableParticles()
base.disableMouse()

input.init(base)

aScene = scene.scene(base)
clock = ClockObject.getGlobalClock()


while True:
    aScene.update(clock.dt)
    
    base.taskMgr.step()