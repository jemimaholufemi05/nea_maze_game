from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import Spotlight, AmbientLight, DirectionalLight
from panda3d.core import Vec4
from panda3d.core import WindowProperties

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        render.setShaderAuto()

        self.environment = loader.loadModel("Models/Misc/environment")
        self.environment.reparentTo(render)

        self.tempActor = Actor("Models/PandaChan/act_p3d_chan", {"walk" : "Models/PandaChan/a_p3d_chan_run"})
        self.tempActor.getChild(0).setH(180)
        self.tempActor.reparentTo(render)
        self.tempActor.loop("walk")

        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)

        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print (controlName, "set to", controlState)


game = Game()
game.run()