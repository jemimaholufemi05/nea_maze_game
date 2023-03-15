from bricks import Bricks
from core.grid import Grid
from core.binary_tree import BinaryTree
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import (
    AmbientLight,
    DirectionalLight,
    Vec4,
    WindowProperties,
    NodePath,
    PandaNode,
)

class Game:

    def __init__(self, grid, base):
        self.grid = grid
        self.init_showBase(base)
        self.init_variables()
        self.init_lighting()
        self.init_window(1000, 750)
        self.init_models()
        self.init_camera()
        self.init_key_map()

        self.updateTask = self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.updateCam, "task_camActualisation", priority=-4)

    def update_key_map(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        dt = globalClock.getDt()
        if self.keyMap["left"]:
            self.player.setH(self.player.getH() + 300 * dt)
        if self.keyMap["right"]:
            self.player.setH(self.player.getH() - 300 * dt)
        if self.keyMap["forward"]:
            self.player.setY(self.player, -25 * dt)
        if self.keyMap["up"]:
            self.player.setZ(self.player.getZ() + 25 * dt)
        if self.keyMap["down"]:
            self.player.setZ(self.player.getZ() - 25 * dt)

        return task.cont

    def init_key_map(self):
        self.keyMap = {
            "left": False,
            "right": False,
            "forward": False,
            "up": False,
            "down": False,
            "center": False,
        }

        self.accept("w", self.update_key_map, ["up", True])
        self.accept("w-up", self.update_key_map, ["up", False])
        self.accept("s", self.update_key_map, ["down", True])
        self.accept("s-up", self.update_key_map, ["down", False])
        self.accept("arrow_left", self.update_key_map, ["left", True])
        self.accept("arrow_right", self.update_key_map, ["right", True])
        self.accept("arrow_up", self.update_key_map, ["forward", True])
        self.accept("arrow_left-up", self.update_key_map, ["left", False])
        self.accept("arrow_right-up", self.update_key_map, ["right", False])
        self.accept("arrow_up-up", self.update_key_map, ["forward", False])
        self.accept("q", self.update_key_map, ["center", True])
        self.accept("q-up", self.update_key_map, ["center", False])

    def init_showBase(self, base):
        self.base = base
        self.render = base.render
        self.win = base.win
        self.accept = base.accept
        self.acceptOnce = base.acceptOnce
        self.taskMgr = base.taskMgr
        self.camera = base.camera
        self.render.setShaderAuto()

    def init_variables(self):
        # a time to keep the cam zoom at a specific speed independent of
        # current framerate
        self._camElapsed = 0.0
        # the next two vars will set the min and max distance the cam can have
        # to the node it is attached to
        self._maxCamDistance = 15.0
        self._minCamDistance = 5.0
        # the initial cam distance
        self._camDistance = (
            self._maxCamDistance - self._minCamDistance
        ) / 2.0 + self._minCamDistance
        # the next two vars set the min and max distance on the Z-Axis to the
        # node the cam is attached to
        self._maxCamHeightDist = 4.0
        self._minCamHeightDist = 2.0
        # the average camera height
        self._camHeightAvg = (
            self._maxCamHeightDist - self._minCamHeightDist
        ) / 2.0 + self._minCamHeightDist
        # the initial cam height
        self._camHeight = self.camHeightAvg
        # a time to keep the cam zoom at a specific speed independent of

    @property
    def maxCamDistance(self):
        return self._maxCamDistance

    @property
    def minCamDistance(self):
        return self._minCamDistance

    @property
    def maxCamHeightDist(self):
        return self._maxCamHeightDist

    @property
    def minCamHeightDist(self):
        return self._minCamHeightDist

    @property
    def camHeightAvg(self):
        return self._camHeightAvg

    @property
    def camDistance(self):
        return self._minCamDistance

    def zoom(self, zoom_in):
        if zoom_in:
            if self.maxCamDistance > self.minCamDistance:
                self.maxCamDistance -= 0.5
            self.acceptOnce("+", self.zoom, [True])
        else:
            if self.maxCamDistance < 15:  # the default maximum
                self.maxCamDistance += 0.5
            self.acceptOnce("-", self.zoom, [False])

    def updateCam(self, task):
        """This function will check the min and max distance of the camera to
        the defined model and will correct the position if the cam is to close
        or to far away
        """
        dt = globalClock.getDt()
        # Camera movement updates
        camvec = self.player.getPos() - self.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()

        # if far from player start following
        if camdist > self.maxCamDistance:
            self.camera.setPos(
                self.camera.getPos() + camvec * (camdist - self.maxCamDistance)
            )
            camdist = self.maxCamDistance
        # If player to close move cam backwards
        if camdist < self.minCamDistance:
            self.camera.setPos(
                self.camera.getPos() - camvec * (self.minCamDistance - camdist)
            )
            camdist = self.minCamDistance
        # get the cameras current offset of the player model on the z-axis
        offsetZ = self.camera.getZ() - self.player.getZ()
        # check if the camera is within the min and max z-axis offset
        if offsetZ < self.minCamDistance:
            # the cam is to low, so move it up
            self.camera.setZ(self.player.getZ() + self.minCamHeightDist)
            offsetZ = self.minCamHeightDist
        elif offsetZ > self.maxCamHeightDist:
            # the cam is to high, so move it down
            self.camera.setZ(self.player.getZ() + self.maxCamHeightDist)
            offsetZ = self.maxCamHeightDist
        # lazy camera positioning
        if offsetZ != self.camHeightAvg:
            # if we are not moving up or down, set the cam to an average position
            if offsetZ != self.camHeightAvg:
                if offsetZ > self.camHeightAvg:
                    # the cam is higher then the average cam height above the player
                    # so move it slowly down
                    self.camera.setZ(self.camera.getZ() - 5 * dt)
                    newOffsetZ = self.camera.getZ() - self.player.getZ()
                    # check if the cam has reached the desired offset
                    if newOffsetZ < self.camHeightAvg:
                        # set the cam z position to exactly the desired offset
                        self.camera.setZ(self.player.getZ() + self.camHeightAvg)
                else:
                    # the cam is lower then the average cam height above the player
                    # so move it slowly up
                    self.camera.setZ(self.camera.getZ() + 5 * dt)
                    newOffsetZ = self.camera.getZ() - self.player.getZ()
                    # check if the cam has reached the desired offset
                    if newOffsetZ > self.camHeightAvg:
                        # set the cam z position to exactly the desired offset
                        self.camera.setZ(self.player.getZ() + self.camHeightAvg)

                    # center the camera as long as the center key is pressed
        if self.keyMap["center"]:
            self.camera.setPos(self.player, 0, camdist, offsetZ)

        # let the camera look at the floater
        self.camera.lookAt(self.camFloater)

        # continue the task until it got manually stopped
        return task.cont

    def init_camera(self):
        self.base.disableMouse()
        self.base.acceptOnce("+", self.zoom, [True])
        self.base.acceptOnce("-", self.zoom, [False])

    def rotate_camera(self, heading, pitch):
        # Get the current camera hpr
        hpr = self.camera.getHpr()

        # Calculate the new hpr values by adding the rotation angles
        new_h = (hpr[0] + heading) % 360
        new_p = max(min(hpr[1] + pitch, 90), -90)  # Limit pitch to -90 to 90 degrees

        # Set the new hpr values
        self.camera.setHpr(new_h, new_p, 0)

    def init_models(self):
        ## self.environment = loader.loadModel("models/Misc/environment")
        # self.environment.reparentTo(render)
        self.bricks = Bricks(root=self.render, columns=False, back_side=True)
        BinaryTree.on(self.grid)
        self.grid.to_png().save("grid_image.png", "PNG", optimize=True)
        self.bricks.load_from_image("grid_image.png")
        self.player = Actor(
            "models/PandaChan/act_p3d_chan", {"walk": "models/PandaChan/a_p3d_chan_run"}
        )
        # self.player.getChild(0).setH(180)
        self.player.reparentTo(self.render)
        self.player.setPos(0, 7, 0)
        self.player.reparentTo(self.render)
        # self.player.setPos(0, 10, 1)
        self.player.reparentTo(self.render)
        self.camFloater = NodePath(PandaNode("playerCamFloater"))
        # the following will set an offset to the node this floater is attached to
        self.camFloater.setPos(0, 0, 1)
        self.camFloater.reparentTo(self.player)
        self.player.loop("walk")

    def init_window(self, width, length):
        self.base.disableMouse()

        properties = WindowProperties()
        properties.setSize(width, length)
        self.win.requestProperties(properties)

    def init_lighting(self):
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = self.render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        self.render.setLight(self.mainLightNodePath)

        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = self.render.attachNewNode(ambientLight)
        self.render.setLight(self.ambientLightNodePath)


if __name__ == "__main__":
    grid = Grid(8, 8)
    base = ShowBase()
    game = Game(grid, base)
    base.run()
