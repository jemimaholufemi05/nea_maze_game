from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import Spotlight, AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import WindowProperties


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        render.setShaderAuto()

        self.init_lighting()
        self.init_window(1000, 750)
        self.init_models()
        self.init_camera()
        self.init_key_map()
        
        self.updateTask = taskMgr.add(self.update, "update")


    def update_key_map(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        dt = globalClock.getDt()

        if self.keyMap["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 5.0 * dt, 0))
        if self.keyMap["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -5.0 * dt, 0))
        if self.keyMap["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0 * dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0 * dt, 0, 0))
        if self.keyMap["shoot"]:
            print("Zap!")

        return task.cont
    
    def init_key_map(self):
        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False,
        }

        self.accept("w", self.update_key_map, ["up", True])
        self.accept("w-up", self.update_key_map, ["up", False])
        self.accept("s", self.update_key_map, ["down", True])
        self.accept("s-up", self.update_key_map, ["down", False])
        self.accept("a", self.update_key_map, ["left", True])
        self.accept("a-up", self.update_key_map, ["left", False])
        self.accept("d", self.update_key_map, ["right", True])
        self.accept("d-up", self.update_key_map, ["right", False])
        self.accept("mouse1", self.update_key_map, ["shoot", True])
        self.accept("mouse1-up", self.update_key_map, ["shoot", False])           

    def init_camera(self):
        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)

    def init_models(self):
        self.environment = loader.loadModel("models/Misc/environment")
        self.environment.reparentTo(render)

        self.tempActor = Actor(
            "models/PandaChan/act_p3d_chan", {"walk": "models/PandaChan/a_p3d_chan_run"}
        )
        self.tempActor.getChild(0).setH(180)
        self.tempActor.reparentTo(render)
        self.tempActor.loop("walk")

    def init_window(self, width, length):
        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(width, length)
        self.win.requestProperties(properties)

    def init_lighting(self):
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)


game = Game()
game.run()
