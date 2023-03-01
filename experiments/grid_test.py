from direct.showbase.ShowBase import ShowBase
from grid import createRandomHeightMapNode
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText 
import sys
class World(ShowBase):
    """docstring for World."""
    def __init__(self):
        #ShowBase.__init__(self)
        self.accept('escape', self.handleEscapeDown)
        self.mTextDisplay = \
            OnscreenText(\
                text = 'Random Heightmap Node Test', \
                pos = (-0.9, 0.9), \
                scale = 0.07, \
                fg = (1,1,0,1),\
                mayChange = True   )
            
        xyscale = 25.0
        zscale = 2.0
        
        base.camLens.setFar(9000)
        base.camLens.setFov(55, 75)
        base.cam.setPos(0, -3*xyscale, xyscale)
        base.cam.setHpr(0, -10, 0)
        
        # Create heightmap node
        xVertexColCount = 8
        yVertexRowCount = 4
        verbose = False
        
        gNode = \
            createRandomHeightMapNode( \
                xVertexColCount, yVertexRowCount, verbose \
            )
        self.mGridNodePath = render.attachNewNode(gNode)
        self.mGridNodePath.setScale(xyscale, xyscale, zscale)
    
        # setup lighting
        lightAttribute = LightAttrib.makeAllOff()
        dirLight = DirectionalLight('DirLight')
        dirLight.setColor(Vec4(0.6, 0.6, 0.6, 1.0))
        dirLightNP = render.attachNewNode(dirLight)
        dirLightNP.setPos(Vec3(0.0, -10.0, 10.0))
        dirLightNP.setHpr(Vec3(0.0, -26.0, 0.0))
        
        lightAttribute = lightAttribute.addLight(dirLight) # add to attribute
        
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(0.25, 0.25, 0.25, 1.0))
        ambientLightNP = render.attachNewNode(ambientLight)
        lightAttribute = lightAttribute.addLight(ambientLight)
        render.node().setAttrib(lightAttribute)
        
    def handleEscapeDown(self):
        sys.exit()
        
world = World()
run()
        