from item import Trader
from map import Map
from player import Player

if __name__ == "__main__":
    print("Wilderness Survival System")

    map = Map(16, 32)
    player = Player("X")

    trader = Trader(4)

    map.add_player((2, 3), player)
    map.populate_items()
    map.add_item((4, 2), trader)
    
    map.draw()
