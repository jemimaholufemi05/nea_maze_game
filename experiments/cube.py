#!/usr/bin/env/ python
import sys
from direct.showbase.ShowBase import ShowBase

from panda3d.core import Geom, GeomNode
from panda3d.core import GeomVertexFormat, GeomVertexWriter, GeomVertexData
from panda3d.core import GeomTriangles
from panda3d.core import NodePath
from panda3d.core import PointLight
from panda3d.core import VBase4
from panda3d.core import AmbientLight
from direct.task import Task
 

class Cube(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Move camera for a better view
        self.disableMouse() 
        # if you leave mouse mode enabled camera position will be governed by Panda mouse control
        self.camera.setY(-10)
        # Enable fast exit
        self.accept("escape", sys.exit)
        
        # create cube
        gNode = self.createCube()
        self.cubeNodePath = self.render.attachNewNode(gNode)
        
        # Add a simple point light
        plight = PointLight('plight')
        plight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(4 , -4, 4)
        self.render.setLight(plnp)
        # Add an ambient light
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        
        # Add the spinCubeTask procedure to the task manager
        self.taskMgr.add(self.spinCubeTask, "spinCubeTask")
        
        # Add the spinCubeTask precedure to the task manager.
    def spinCubeTask(self, task):
        angleDegrees = task.time * 6.0
        self.cubeNodePath.setHpr(angleDegrees, angleDegrees, angleDegrees)
        return Task.cont
    
    
    
    def createCube(self):
        format = GeomVertexFormat.getV3n3c4()
        vertexData = GeomVertexData('cube', format, Geom.UHStatic)
        
        vertexData.setNumRows(24)
        vertices = GeomVertexWriter(vertexData, 'vertex')
        normals = GeomVertexWriter(vertexData, 'normal')
        colors = GeomVertexWriter(vertexData, 'color')
        
        vertices.addData3f(-1, -1, -1)
        vertices.addData3f(-1, -1, -1)
        vertices.addData3f(-1, -1, -1)
        vertices.addData3f(1, -1, -1)
        vertices.addData3f(1, -1, -1)
        vertices.addData3f(1, -1, -1)
        vertices.addData3f(1, 1, -1) 
        vertices.addData3f(1, 1, -1) 
        vertices.addData3f(1, 1, -1) 
        vertices.addData3f(-1, 1, -1)
        vertices.addData3f(-1, 1, -1)
        vertices.addData3f(-1, 1, -1)
        vertices.addData3f(-1, -1, 1)
        vertices.addData3f(-1, -1, 1)
        vertices.addData3f(-1, -1, 1)
        vertices.addData3f(1, -1, 1) 
        vertices.addData3f(1, -1, 1) 
        vertices.addData3f(1, -1, 1) 
        vertices.addData3f(1, 1, 1)
        vertices.addData3f(1, 1, 1)
        vertices.addData3f(1, 1, 1)
        vertices.addData3f(-1, 1, 1) 
        vertices.addData3f(-1, 1, 1) 
        vertices.addData3f(-1, 1, 1) 

        normals.addData3f(0, -1, 0)
        normals.addData3f(-1, 0, 0)
        normals.addData3f(0, 0, -1)
        normals.addData3f(0, -1, 0)
        normals.addData3f(1, 0, 0)
        normals.addData3f(0, 0, -1)
        normals.addData3f(1, 0, 0)
        normals.addData3f(0, 1, 0)
        normals.addData3f(0, 0, -1)
        normals.addData3f(0, 1, 0)
        normals.addData3f(-1, 0, 0)
        normals.addData3f(0, 0, -1)
        normals.addData3f(0, -1, 0)
        normals.addData3f(-1, 0, 0)
        normals.addData3f(0, 0, 1)
        normals.addData3f(0, -1, 0)
        normals.addData3f(1, 0, 0)
        normals.addData3f(0, 0, 1)
        normals.addData3f(1, 0, 0)
        normals.addData3f(0, 1, 0)
        normals.addData3f(0, 0, 1)
        normals.addData3f(0, 1, 0)
        normals.addData3f(-1, 0, 0)
        normals.addData3f(0, 0, 1)

        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        colors.addData4f(0, 0, 1, 1)
        
        # Store the triangles, counter clockwise from front
        primitive = GeomTriangles(Geom.UHStatic)
        primitive.addVertices(0, 3, 15)
        primitive.addVertices(0, 15, 12)
        primitive.addVertices(4, 6, 18)
        primitive.addVertices(4, 18, 16)
        primitive.addVertices(7, 9, 21)
        primitive.addVertices(7, 21, 19)
        primitive.addVertices(10, 1, 13)
        primitive.addVertices(10, 13, 22)
        primitive.addVertices(2, 11, 8)
        primitive.addVertices(2, 8, 5)
        primitive.addVertices(14, 17, 20)
        primitive.addVertices(14, 20, 23)

        geom = Geom(vertexData)
        geom.addPrimitive(primitive)

        node = GeomNode('cube gnode')
        node.addGeom(geom)
        return node

app = Cube()
app.run()
        