#! usr/bin/env python

import sys
import math
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

class Prism(ShowBase):
    def __init__(self):
        super().__init__(self)

        # Move camera for a better view
        self.disableMouse() # if you leave mouse mode enabled camera position will be governed by Panda mouse control
        self.camera.setY(- 10)

        # Enable fast exit
        self.accept("escape", sys.exit)

        # Create prism
        gNode = self.createPrism()
        self.prismNodePath = self.render.attachNewNode(gNode)

        # Add a simple point light
        plight = PointLight('plight')
        plight.setColor(VBase4(0.5, 0.5, 0.5, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(4, -4, 4)
        self.render.setLight(plnp)
        # Add an ambient light
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # Add the spinPrismTask procedure to the task manager.
        self.taskMgr.add(self.spinPrismTask, "spinPrismTask")

    def spinPrismTask(self, task):
        angleDegrees = task.time * 6.0
        self.prismNodePath.setHpr(angleDegrees, angleDegrees, angleDegrees)
        return Task.cont

    def normal_2D(self, p1, p2):
        # Mapping is y2 = p2[1], x2 = p2[0],  y1 = p1[1], x1 = p1[0]
        x_diff = p2[0] - p1[0]
        y_diff = p2[1] - p1[1]
        hyp = math.sqrt(x_diff * x_diff + y_diff * y_diff)
        # right hand normal circulating counter clockwise
        return [y_diff / hyp, -x_diff / hyp]

    def rotate_by_1(self, my_list):
        return my_list[1:] + my_list[:1]

    def calcNormals(self, points):
        return [self.normal_2D(p1, p2) for p1, p2 in zip(points, self.rotate_by_1(points))]

    def createPrism(self):
        # 2D Polygon and its 2D normals
        # xys = [[-3, -1], [3, -1], [3, 1], [-3, 1]]  # railway sleeper
        # xys = [[-1, -2], [0, -1], [1, -2], [2, -1], [1, 0], [2, 1],
        #        [1, 2], [0, 1], [-1, 2], [-2, 1], [-1, 0], [-2, -1]]  # cross - tesselation doesn't work
        # xys = [[-1, -2], [1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1]]  # octagonal prism
        xys = [[-1, -1], [1, -1], [1, 1], [0, 2], [-1, 1]]  # monopoly board house
        #xys = [[-1, -1], [1, -1], [1, 1], [0, 0], [-1, 1]]  # georgian terrace - inverted roof
        xy_normals = self.calcNormals(xys)

        """
        Coverage triangle indices for the top polygonal face (counter clockwise - illustrated) and
        bottom polygonal face (clockwise - not shown). Fails for some concave polygons like the cross.

                    .4        
                    .  \
                    .   .3
                    .  .  |                        
                . .   .2
                .. .   /
                0 --- 1
        """
        tri_top = [[0, vix+1, vix+2] for vix in range(len(xys) - 2)]
        tri_bot = [[0, vix-1, vix-2] for vix in range(len(xys), 2, -1)]

        # To hold vertex numbers belonging to the rectangular faces whose normals are xy normals
        rects = {}

        """
        Forward (counter clockwise) and back (clockwise) triangle indices for covering rectangular faces
                2 --------- 3
                |  b     f  |
                |     x     |
                |  f     b  |
                0 --------- 1
        """
        tri_fwd = [[0, 1, 3], [0, 3, 2]]
        tri_back = [[1, 0, 2], [1, 2, 3]]

        # Bottom face then top face
        zs = [-1, 1]

        # To hold vertex numbers belonging to the bottom and top faces
        polys = {}

        # All the vertex positions of the solid
        xyzs = [xy + [z] for z in zs for xy in xys]

        # There must be 3 separate vertices at each vertex position, each with a different normal,
        # which always points outwards from the solid
        format = GeomVertexFormat.getV3n3c4()
        vertexData = GeomVertexData('prism', format, Geom.UHStatic)
        vertexData.setNumRows(3 * len(xyzs))

        vertices = GeomVertexWriter(vertexData, 'vertex')
        normals = GeomVertexWriter(vertexData, 'normal')
        colors = GeomVertexWriter(vertexData, 'color')

        for pos_num, xyz in enumerate(xyzs):
            edge_fwd = pos_num % len(xys)
            edge_back = (edge_fwd - 1) % len(xys)
            edge_nums = [edge_back, edge_fwd]
            for i in range(3):
                vertices.addData3f(*xyz)
                vnum = pos_num * 3 + i
                if i in [0, 1]:
                    edge_num = edge_nums[i]
                    normal = xy_normals[edge_num] + [0]
                    rects.setdefault(edge_num, []).append(vnum)
                else:
                    z_vec = xyz[2]
                    normal = [0, 0, z_vec]
                    polys.setdefault(z_vec, []).append(vnum)

                normals.addData3f(*normal)
                colors.addData4f(0, 0, 1, 1)

        # Store the tessellation triangles, counter clockwise from front.
        # Each vertex assigned to a triangle must have a normal vector that
        # points outwards from the triangle face, which thus determines which
        # of the 3 possible vertexes to chose at any given vertex position.
        # Each triangle's vertices should be specified in counter clockwise
        # order from the perspective of the vertices' normals (i.e. looking at the
        # outside of the face).
        primitive = GeomTriangles(Geom.UHStatic)

        # Cover the rectangular faces around the edges
        for edge_num in rects:
            # cater for wrap around back to the zeroth edge number
            tri_ix_pairs = tri_back if edge_num == (len(xys) - 1) else tri_fwd
            for tri_ixs in tri_ix_pairs:
                vnums = [rects[edge_num][tri_ix] for tri_ix in tri_ixs]
                primitive.addVertices(*vnums)

        # Cover the polygonal faces on the top and bottom
        for poly in polys:
            # Use clockwise indexing on the bottom (negative normal) face and
            # counter clockwise on the top (positive normal) face
            faces = tri_bot if poly < 0 else tri_top
            for tri_ixs in faces:
                vnums = [polys[poly][tri_ix] for tri_ix in tri_ixs]
                primitive.addVertices(*vnums)

        geom = Geom(vertexData)
        geom.addPrimitive(primitive)

        node = GeomNode('triangular prism gnode')
        node.addGeom(geom)
        return node


app = Prism()
app.run()
