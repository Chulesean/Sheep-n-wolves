# Sheep-n-wolves
Game Components
Board: 8×8 chessboard (using only the black squares/diagonal movement)

Pieces:
1 Wolf
4 Sheep

Initial Setup
Wolf: Starts at the middle of the bottom row (position varies, typically (3,0) or (4,0) in 0-based indexing)
Sheep: Start on the top row, usually on alternating black squares (e.g., (1,7), (3,7), (5,7), (7,7))

Movement Rules
Wolf Movement
Can move one square diagonally in any direction (forward or backward)
Movement pattern similar to a chess bishop but only one square
Example moves: (3,0) → (2,1) or (4,1) or (2,-1) [if valid]

Sheep Movement
Can move one square diagonally but only forward (toward the wolf's starting side)
Cannot move backward or sideways
Example: (1,7) → (0,6) or (2,6)

Win Conditions
Wolf Wins If:
Reaches any square on the top row (the sheep's starting side)
The wolf wins by escaping past the sheep line

Sheep Win If:
Block the wolf completely so it has no legal moves
The sheep win by surrounding/trapping the wolf

Additional Rules
No capturing/jumping: Pieces cannot capture or jump over each other
Alternating turns: Wolf moves first, then sheep, alternating
Mandatory movement: Players must make a move if possible
No passing: Players cannot skip their turn

Strategic Elements
Sheep strategy: Form connected lines to block the wolf's advance
Wolf strategy: Find gaps in the sheep formation to break through
Key positions: Control central diagonal pathways

Special Notes
Only black squares are used for movement (like in checkers)
All movement is diagonal only
The game is asymmetric - wolf has more mobility but is outnumbered
