import os
from player import Player
from screen import Screen 
from controller import Controller
import timer_2 

class Game:
    def clear(self):
        os.system('cls')
        
    def __init__(self):
        self.player = Player()
        self.screen = Screen()
        self.controller = Controller()
    
    
    def run(self):
        while True:
            self.screen.render(self.player)
            self.player.move(*self.controller.read())
            self.clear()
            
if __name__ == "__main__":
    try:
        start = timer_2.start_timer()
        game = Game()
        game.run()
    except KeyboardInterrupt:
        timer_2.end_timer(start)
        pass