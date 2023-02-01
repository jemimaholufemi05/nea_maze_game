class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[self.root] = 0
    
    def dist(self, cell):
        return self.cells[cell]
    
    def dist(self, cell, distance):
        self.cells[cell] = distance
        
    def cells(self):
        return self.cells.keys()
    
    def path_to(self, goal):
        current = goal
        
        breadcrumbs = Distances(self.root)
        breadcrumbs.dist(self.cells[current])
        
        while not current = self.root:
            for neighbour in current.links:
                if self.cells[neighbour] = self.cells[current]:
                    breadcrumbs.dist