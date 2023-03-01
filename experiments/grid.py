from direct.gui.OnscreenText import OnscreenText 
import direct.directbase.DirectStart
from direct.task import Task
import sys
from panda3d.core import *
import random

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

def createRandomHeightMapNode(xVertexColCount,yVertexRowCount,verbose) :

	# Define the vetex data format (GVF). 
	gvf = GeomVertexFormat.getV3n3c4t2 ()

	# Create the vetex data container (GVD) using the GVF from above to
	# describe its contents.
	gvd = GeomVertexData('GridVertices',gvf,Geom.UHStatic)

	# Create writers for the GVD, one for each type of data (column) that
	# we are going to store in it.
	gvwV = GeomVertexWriter(gvd, 'vertex')
	gvwT = GeomVertexWriter(gvd, 'texcoord')
	gvwC = GeomVertexWriter(gvd, 'color')
	gvwN = GeomVertexWriter(gvd, 'normal')

	# Use the writers to add vertex data to the GVD.

	xColOffset = float(xVertexColCount-1)*0.5
	yRowOffset = float(yVertexRowCount-1)*0.5

	xColScale = 1.0 / float(xVertexColCount)
	yRowScale = 1.0 / float(yVertexRowCount)

	if verbose :
		print("Rows, Row Offset : ",yVertexRowCount,yRowOffset)
		print("Cols, Col Offset : ",xVertexColCount,xColOffset)

	# Compute function for computation of texture coordinates. This
	# will map the range (0,yVertexRowCount-1) onto (0,1) and it
	# will map the range (0,xVertexColCount-1) onto (0,1)
	xTexSlope = 1.0 / float(xVertexColCount-1)
	yTexSlope = 1.0 / float(yVertexRowCount-1)

	k = 0
	gRan = random.Random(5033)
	for yRow in range(0, yVertexRowCount): 

		if verbose :
			print("Creating Vertices in Row ",yRow," with ",\
				xVertexColCount," vertices in the column")

		y = yRowScale*(float(yRow) - float(yRowOffset))
		ty = yRow*yTexSlope

		for xCol in range(0, xVertexColCount): 

			z = gRan.random()
			x = xColScale*(float(xCol) - float(xColOffset))
			tx = xCol*xTexSlope

			gvwV.addData3f(x, y, z)
			gvwN.addData3f(0, 0, 1)
			gvwC.addData4f(0, z, z, 1)
			gvwT.addData2f(tx, ty)

			if verbose :
				print("\tVert Col(%d) : %f,%f,%f" % (k,x, y, z))
				k = k + 1

	# Create a GeomPrimitive object to use the vertices in the GVD
	# then fill it with our grid data.

	geom = Geom(gvd)

	xTriangleColCount = xVertexColCount - 1
	yTriangleRowCount = yVertexRowCount - 1

	for yRow in range(0, yTriangleRowCount) :

		if verbose :
			print("Creating Triangles in Row ",yRow," with ", \
				xTriangleColCount, " triangle pairs in the column")

		for xCol in range(0, xTriangleColCount):

			tris = GeomTriangles(Geom.UHStatic)

			v0 = yRow*xVertexColCount + xCol
			v1 = v0 + 1
			v2 = v1 + xVertexColCount
			v3 = v2 - 1

			tris.addVertex(v0)
			tris.addVertex(v1)
			tris.addVertex(v2)
			tris.closePrimitive()

			tris.addVertex(v0)
			tris.addVertex(v2)
			tris.addVertex(v3)
			tris.closePrimitive()

			geom.addPrimitive(tris)

			if verbose :
				print("\tTris : %d,%d,%d   %d,%d,%d" % (v0,v1,v2, v0,v2,v3))

	node = GeomNode('grid')
	node.addGeom(geom)

	return node