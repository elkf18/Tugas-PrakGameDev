from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


keyMap={
    "up":False,
    "down":False,
    "left":False,
    "right":False,
    "rotate":False,

}

def updateKeyMap(key, state):
    keyMap[key]=state
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()
        
        # meload  environment model.
        self.scene = self.loader.loadModel("models/environment")
        # merender model
        self.scene.reparentTo(self.render)
        # mengaplikasikan scale dan transformasi posisi di model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # menambahkan spinCameraTask 
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # meload dan transformasi aktor panda .
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        # membuat fungsi keybooard event
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])

        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])

        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])

        self.accept("space", updateKeyMap, ["rotate", True])
        self.accept("space-up", updateKeyMap, ["rotate", False])

        # untuk kecepatan dan angle nya
        self.speed=4
        self.angle=0

        # mengusdate task manager
        self.taskMgr.add(self.update, "update")

        # melooping panda nya
        self.pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        # posInterval1 = self.pandaActor.posInterval(13,
        #                                            Point3(0, -10, 0),
        #                                            startPos=Point3(0, 10, 0))
        # posInterval2 = self.pandaActor.posInterval(13,
        #                                            Point3(0, 10, 0),
        #                                            startPos=Point3(0, -10, 0))
        # hprInterval1 = self.pandaActor.hprInterval(3,
        #                                            Point3(180, 0, 0),
        #                                            startHpr=Point3(0, 0, 0))
        # hprInterval2 = self.pandaActor.hprInterval(3,
        #                                            Point3(0, 0, 0),
        #                                            startHpr=Point3(180, 0, 0))

        # # Create and play the sequence that coordinates the intervals.
        # self.pandaPace = Sequence(posInterval1, hprInterval1,
        #                           posInterval2, hprInterval2,
        #                           name="pandaPace")
        # self.pandaPace.loop()

        # meload audio
        self.loadAudio()
    
    # fungsi update
    def update(self,task):
        dt=globalClock.getDt()

        # mengeset posisi panda
        pos = self.pandaActor.getPos()

        if keyMap["left"]:
            pos.x -= self.speed *dt
        if keyMap["right"]:
            pos.x += self.speed *dt
        if keyMap["up"]:
            pos.z += self.speed *dt
        if keyMap["down"] and pos.z > 0:
            pos.z -= self.speed * dt
        if keyMap["rotate"]:
            self.angle += 1
            self.pandaActor.setH(self.angle)
        
        self.pandaActor.setPos(pos)

        return task.cont

    # meload audio
    def loadAudio(self):
        music = self.loader.loadMusic("suara.mp3")
        music.play()
        music.setVolume(.5)
        music.setLoopCount(2)

    # fungsi untuk memindahkan kamera
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
