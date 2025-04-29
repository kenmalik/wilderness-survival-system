from item import Trader
from map import Map
from player import Player
from console import console

if __name__ == "__main__":
    console.rule("Wilderness Survival System")
    print()

    map = Map(16, 64)
    player = Player("P")

    trader = Trader(4)

    map.add_player((2, 3), player)
    map.populate_items()
    map.add_item((4, 2), trader)
    
    map.draw()
    print()
