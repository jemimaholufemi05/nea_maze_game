# u : (0,1) this moves the player up one space
# d : (0,-1) this moves the player down one space
# r : (1,0) this moves the player right one space
# l : (-1,0) this moves the player left one space
import timer_2

class Player:
   def __init__(self):
       self.x = 1
       self.y = 1
   def move(self,dx,dy):
       # move player to some position 
       # param dx how much to move in the x axis 
       # param dy how much to move in the y axis
       if (self.x + dx) < 1 or (self.y + dy) < 1 :
            self.x = 1
            self.y = 1
            return 
        
       self.x += dx
       self.y += dy
       
if __name__ == "__main__":        
    def main():
        start = timer_2.start_timer()
        player = Player()
        while True:
            x = int(input("move along the x axis: "))
            y = int(input("move along the y axis: "))
            player.move(x,y)
            print(f"player's x position is {player.x}")
            print(f"player's y position is {player.y}")
            
        timer_2.end_timer(start)
    main()