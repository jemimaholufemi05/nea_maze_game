from collections import defaultdict
import itertools
from panda3d.core import Vec3, GeomVertexReader, LineSegs

class NavGraph:
    def __init__(
        self,
        mesh,
        smooth=0.5,
        edge_neighbors_only=True,
        max_moves=None,
        debug=False,
        draw_graph=False,
    ) -> None:
        self.debug = debug
        self.smooth_factor = smooth
        self.max_moves = max_moves

    def _round_vec3_to_tuple(self, vec):
        return tuple([round(x * 4.0) / 4.0 for x in vec])

    def _distance(self, start: Vec3, end: Vec3):
        return (end - start).lengthSquared()

    def _get_center(self, vertex):
        return Vec3(
            (vertex[0][0] + vertex[1][0] + vertex[2][0]) / 3.0,
            (vertex[0][1] + vertex[1][1] + vertex[2][1]) / 3.0,
            (vertex[0][2] + vertex[1][2] + vertex[2][2]) / 3.0,
        )

    def find_first_geom(self, mesh):
        for child in mesh.getChildren():
            node = child.node()
            if node.isGeomNode():
                return node.getGeom(0)

    def _get_neighbors(self, vertex, vert_dict, triangle_id, edge_only=True):
        common = set()
        if edge_only:
            for pair in itertools.combinations(vertex, 2):
                common = common | vert_dict[pair[0]] & vert_dict[pair[1]]
        else:
            for vert_id in vertex:
                common = common | vert_dict[vert_id]
        common = common - {triangle_id}
        return list(common)

    def draw_connections(self):
        try:
            self.visual.removeNode()
        except:
            pass
        else:
            line = LineSegs()
            line.setColor(1, 0, 0, 1)
            line.setThickness(2)
            for start_node, ends in self.graph["neighbors"].items():
                start_pos = self.graph["pos"][start_node]
                for end in ends:
                    end_pos = self.graph["pos"][end]
                    line.moveTo(start_pos)
                    line.drawTo(end_pos)
        self.visual = render.attachNewNode(line.create())

    def make_nav_graph(self, mesh, edge_neighbors_only=True, draw_graph=False):
        """
        Creates a navigation graph from a 3D mesh, A node is created for each triangle
        in the mesh, nodes are connected either by shared edges (edge_neighbors_only=True),
        or by shared vertex (edge_neighbors_only=False).
        """

        triangles = []
        vert_dict = defaultdict(set)
        geom = self.find_first_geom(mesh)

        vdata = geom.getVertexData()
        vertex = GeomVertexReader(vdata, "vertex")
        for prim in geom.getPrimitives():
            num_primitives = prim.getNumPrimitives()
            for p in range(num_primitives):
                start = prim.getPrimitiveStart(p)
                end = prim.getPrimitiveEnd(p)
                triangle = {"vertex_id": [], "vertex_pos": []}
                for i in range(start, end):
                    vi = prim.getVertex(i)
                    vertex.setRow(vi)
                    v = [round(i, 4) for i in vertex.getData3f()]
                    vertex_id = tuple([round(i * 4.0) / 4.0 for i in v])
                    triangle["vertex_pos"].append(v)
                    triangle["vertex_id"].append(vertex_id)
                    vert_dict[vertex_id].add(len(triangles))
                triangles.append(triangle)

        # get centers and neighbors
        for i, triangle in enumerate(triangles):
            triangle["center"] = self._get_center(triangle["vertex_pos"])
            triangle["neighbors"] = self._get_neighbors(
                triangle["vertex_id"], vert_dict, i, edge_neighbors_only
            )

        edges = {}
        cost = {}
        positions = {}

        for i, triangle in enumerate(triangles):
            edges[i] = triangle["neighbors"]
            cost[i] = {}
            start = triangle["center"]
            positions[i] = start
            for neighbor in triangle["neighbors"]:
                cost[i][neighbor] = self._distance(start, triangles[neighbor]["center"])
        lookup = {
            self._round_vec3_to_tuple(value): key for (key, value) in positions.items()
        }
        self.graph = {
            "neighbors": edges,
            "cost": cost,
            "pos": positions,
            "lookup": lookup,
        }

        draw_graph and self.draw_connections()
