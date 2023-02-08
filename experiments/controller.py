class Controller:
# u : (0,1) this moves the player up one space
# d : (0,-1) this moves the player down one space
# r : (1,0) this moves the player right one space
# l : (-1,0) this moves the player left one space
    MOVE = {
    "u": (0,-1),
    "d": (0,1),
    "r": (1,0),
    "l": (-1,0)
    }
# to use arrow keys to move, do pip install pynput
    NO_MOVE = (0,0)
    
    def read(self):
        return self.MOVE.get(input("Move player: "), self.NO_MOVE)