"""
Represents the geometric layout of the Nine Men's Morris board.

This class handles all board-related geometry including point coordinates,
connections between points, adjacency lists for move validation, and mill formations.
"""

from typing import Tuple, List, Dict, Set

class BoardGeometry:
    """Board geometry for Nine Men's Morris game."""
    
    RING_SIZE = 8
    TOTAL_POINTS = 24
    NUM_RINGS = 3

    def __init__(self, board_half: int, cx: int, cy: int) -> None:
        # Input validation
        if board_half <= 0:
            raise ValueError(f"board_half must be positive, got {board_half}")
        
        if not isinstance(cx, (int, float)):
            raise TypeError(f"cx must be numeric, got {type(cx).__name__}")
        
        if not isinstance(cy, (int, float)):
            raise TypeError(f"cy must be numeric, got {type(cy).__name__}")
        
        # Convert to int if float
        self.cx = int(cx)
        self.cy = int(cy)
        self.outer = board_half
        self.middle = board_half * 2 // 3
        self.inner = board_half // 3
        self.points = self.generate_points()
        self.connections, self.adjacency = self.generate_connections()
        self.mills = self.generate_mills()
    
    def square_points(self, dist: int) -> List[Tuple[int, int]]:
        """
        Generate 8 points forming a square at given distance from center.
        
        Args:
            dist (int): Distance from center to the square.
            
        Returns:
            list: List of 8 (x, y) coordinates in clockwise order
                  starting from top-left corner.
        """
        return [
            (self.cx - dist, self.cy - dist),   # top-left
            (self.cx, self.cy - dist),          # top-middle
            (self.cx + dist, self.cy - dist),   # top-right
            (self.cx + dist, self.cy),          # right-middle
            (self.cx + dist, self.cy + dist),   # bottom-right
            (self.cx, self.cy + dist),          # bottom-middle
            (self.cx - dist, self.cy + dist),   # bottom-left
            (self.cx - dist, self.cy)           # left-middle
        ]
    
    def generate_points(self) -> List[Tuple[int, int]]:
        """Generate all 24 board points."""
        outer_pts = self.square_points(self.outer)
        middle_pts = self.square_points(self.middle)
        inner_pts = self.square_points(self.inner)
        return outer_pts + middle_pts + inner_pts
    
    def generate_connections(self) -> Tuple[List[Tuple[int, int]], Dict[int, Set[int]]]:
        """Generate connections and adjacency list."""
        connections = []
        adjacency = {i: set() for i in range(self.TOTAL_POINTS)}
        
        # Ring connections
        for ring in range(self.NUM_RINGS):
            base = ring * self.RING_SIZE
            for i in range(self.RING_SIZE):
                a = base + i
                b = base + (i + 1) % self.RING_SIZE
                connections.append((a, b))
                adjacency[a].add(b)
                adjacency[b].add(a)
        
        # Cross connections
        for i in (1, 3, 5, 7):
            connections.append((i, i + self.RING_SIZE))
            connections.append((i + self.RING_SIZE, i + 2 * self.RING_SIZE))
            adjacency[i].add(i + self.RING_SIZE)
            adjacency[i + self.RING_SIZE].add(i)
            adjacency[i + self.RING_SIZE].add(i + 2 * self.RING_SIZE)
            adjacency[i + 2 * self.RING_SIZE].add(i + self.RING_SIZE)
        
        return connections, adjacency
    
    def generate_mills(self) -> List[Tuple[int, int, int]]:
        """Generate all possible mill formations."""
        mills = []
        
        # Horizontal mills for each ring (4 mills per ring × 3 rings = 12 mills)
        for ring in range(self.NUM_RINGS):
            base = ring * self.RING_SIZE
            for i in range(0, self.RING_SIZE, 2):  # Step by 2 to get corners
                # Each horizontal mill consists of 3 consecutive points
                p1 = base + i
                p2 = base + (i + 1) % self.RING_SIZE
                p3 = base + (i + 2) % self.RING_SIZE
                mills.append((p1, p2, p3))
        
        # Vertical mills across rings (4 mills total)
        # These use the middle points: indices 1, 3, 5, 7 of each ring
        for i in [1, 3, 5, 7]:
            p1 = i                    # Outer ring
            p2 = i + self.RING_SIZE    # Middle ring
            p3 = i + 2 * self.RING_SIZE  # Inner ring
            mills.append((p1, p2, p3))
        
        return mills
    
