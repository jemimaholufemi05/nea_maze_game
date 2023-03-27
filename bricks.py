from panda3d.core import NodePath, PNMImage, CollisionNode, CollisionBox, BitMask32


class Bricks:
    @property
    def level(self):
        return self._level

    """docstring for Bricks."""

    def __init__(self, base, columns, back_side=False):
        self.base = base
        self.root = base.render
        self.columns = columns
        self.base_side = back_side
        self.base_bricks = self.load_base_bricks()
        self.exit_placement = self.map_exits()
        self.load_bricks_with_corresponding_exits(self.exit_placement)
        self._level = self.root.attach_new_node("level")
        self.layout = {}
        self.vis = None

    def load_base_bricks(self):
        return {
            "column1": loader.load_model("models/column1.bam"),
            "column2": loader.load_model("models/column2.bam"),
            "column3": loader.load_model("models/column3.bam"),
            "column4": loader.load_model("models/column4.bam"),
            "floor": loader.load_model("models/floor.bam"),
            "wall": loader.load_model("models/wall.bam"),
            "nav_mesh": loader.load_model("models/nav_mesh.bam"),
            "nav_mesh_base": loader.load_model("models/nav_mesh_base.bam"),
        }

    def map_exits(self):
        # key: exit placement /90deg
        return {
            frozenset((0, 1, 2, 3, 4)): NodePath("brick_with_4_exits"),
            frozenset((0, 1, 2)): NodePath("brick_with_3_exits_west_walled"),
            frozenset((0, 1, 3)): NodePath("brick_with_3_exits_south_walled"),
            frozenset((0, 2, 3)): NodePath("brick_with_3_exits_east_walled"),
            frozenset((1, 2, 3)): NodePath("brick_with_3_exits_north_walled"),
            frozenset((0, 1)): NodePath("brick_with_2_exits_south_west_walled"),
            frozenset((0, 2)): NodePath("brick_with_2_exits_east_west_walled"),
            frozenset((0, 3)): NodePath("brick_with_2_exits_east_south_walled"),
            frozenset((1, 2)): NodePath("brick_with_2_exits_north_west_walled"),
            frozenset((2, 3)): NodePath("brick_with_2_exits_north_east_walled"),
            frozenset((1, 3)): NodePath("brick_with_2_exits_north_south_walled"),
            frozenset((0,)): NodePath("brick_with_1_exit_east_south_west_walled"),
            frozenset((1,)): NodePath("brick_with_1_exit_north_south_west_walled"),
            frozenset((2,)): NodePath("brick_with_1_exit_north_east_west_walled"),
            frozenset((3,)): NodePath("brick_with_1_exit_north_east_south_walled"),
            frozenset(): NodePath("brick_zero_exit"),
        }

    def load_bricks_with_corresponding_exits(self, map_exits):
        for exit_rotation, brick in map_exits.items():
            # add columns to the brick
            self.columns and [
                self.base_bricks[col].copy_to(brick)
                for col in "column1 column2 column3 column4".split()
            ]

            # add floor to the brick
            self.base_bricks["floor"].copy_to(brick)

            # add walls to the brick
            wall_rotation = set((0, 1, 2, 3)) - exit_rotation
            for h in wall_rotation:
                wall = self.base_bricks["wall"].copy_to(brick)
                wall.set_h(h * 90)
                self.base_side and wall.setTwoSided(True)
            # flatten the brick and add a nav mesh
            brick.clear_model_nodes()
            brick.flatten_strong()
            nav = brick.attach_new_node("nav")
            self.base_bricks["nav_mesh_base"].copy_to(nav)

            for h in exit_rotation:
                walk = self.base_bricks["nav_mesh"].copy_to(nav)
                walk.set_h(h * 90)

            brick.clear_model_nodes()
            nav.flatten_strong()
            nav.hide()

    def generate(self, NavGraph, trav, queue, brick_size=4):
        for (x, y), brick in self.layout.items():
            brick_node = self.exit_placement[brick].copy_to(self.level)
            brick_node.set_pos(x * brick_size, y * brick_size, 0)

            brick_collision_node = CollisionNode(f"brick_collision_node_{x}_{y}")
            brick_collision_node.set_into_collide_mask(BitMask32.bit(1))
            brick_collision_node.set_from_collide_mask(BitMask32.bit(1))

            brick_collision_box = CollisionBox(
                (-brick_size / 2, -brick_size / 2, 0),
                (brick_size / 2, brick_size / 2, brick_size),
            )
            brick_collision_node.add_solid(brick_collision_box)

            brick_collision_node_path = brick_node.attach_new_node(brick_collision_node)
            trav.add_collider(brick_collision_node_path, queue)

        nav_mesh = NodePath("navmesh")
        for node in self.level.find_all_matches("**/nav"):
            node.wrt_reparent_to(nav_mesh)

        nav_mesh.flatten_strong()
        self.navgraph = NavGraph(mesh=nav_mesh.get_child(0), draw_graph=False)
        nav_mesh.remove_node()

        self.level.flatten_strong()

    def make_brick_at(self, x, y):
        if (x, y) not in self.layout:
            return

        brick_type = []
        if (x, y + 1) in self.layout:
            brick_type.append(0)
        if (x - 1, y) in self.layout:
            brick_type.append(1)
        if (x, y - 1) in self.layout:
            brick_type.append(2)

        self.layout[(x, y)] = frozenset(brick_type)

    def add(self, x, y):
        self.layout[(x, y)] = None
        self.make_brick_at(x, y)
        self.make_brick_at(x - 1, y)
        self.make_brick_at(x + 1, y)
        self.make_brick_at(x + 1, y)
        self.make_brick_at(x, y - 1)
        self.make_brick_at(x, y + 1)

    def load_from_image(self, NavGraph, trav, pusher, img_file):
        img = PNMImage()
        img.read(img_file)
        for x in range(img.get_x_size()):
            for y in range(img.get_y_size()):
                img.get_gray(x, y) < 0.5 and self.add(x, y)

        self.generate(NavGraph, trav, pusher)
