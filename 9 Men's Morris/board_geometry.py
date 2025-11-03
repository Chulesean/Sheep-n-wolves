class BoardGeometry:
    def __init__(self, board_half, cx, cy):
        self.cx = cx
        self.cy = cy
        self.outer = board_half
        self.middle = int(board_half * 2 / 3)
        self.inner = int(board_half * 1 / 3)
        self.points = self.generate_points()
        self.connections, self.adjacency = self.generate_connections()
        self.mills = self.generate_mills()
    
    def square_points(self, dist):
        return [
            (self.cx - dist, self.cy - dist), (self.cx, self.cy - dist), (self.cx + dist, self.cy - dist),
            (self.cx + dist, self.cy), (self.cx + dist, self.cy + dist), (self.cx, self.cy + dist),
            (self.cx - dist, self.cy + dist), (self.cx - dist, self.cy)
        ]
    
    def generate_points(self):
        outer_pts = self.square_points(self.outer)
        middle_pts = self.square_points(self.middle)
        inner_pts = self.square_points(self.inner)
        return outer_pts + middle_pts + inner_pts
    
    def generate_connections(self):
        connections = []
        adjacency = {i: set() for i in range(24)}
        
        # Ring connections
        for base in (0, 8, 16):
            for i in range(8):
                a, b = base + i, base + (i + 1) % 8
                connections.append((a, b))
                adjacency[a].add(b)
                adjacency[b].add(a)
        
        # Cross connections
        for i in (1, 3, 5, 7):
            connections.append((i, i + 8))
            connections.append((i + 8, i + 16))
            adjacency[i].add(i + 8)
            adjacency[i + 8].add(i)
            adjacency[i + 8].add(i + 16)
            adjacency[i + 16].add(i + 8)
        
        return connections, adjacency
    
    def generate_mills(self):
        return [
            (0,1,2), (2,3,4), (4,5,6), (6,7,0),
            (8,9,10), (10,11,12), (12,13,14), (14,15,8),
            (16,17,18), (18,19,20), (20,21,22), (22,23,16),
            (1,9,17), (3,11,19), (5,13,21), (7,15,23)
        ]