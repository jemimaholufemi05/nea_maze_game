class Screen:
    def render(self,player):
        print("\n" * player.y)
        print(player.x * " " + "  0 ")
        print(player.x * " " + "  T ")
        print(player.x * " " + " / \ ")
        print(" ")