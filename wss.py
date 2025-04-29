from item import GoldBonus, FoodBonus, WaterBonus, Trader
from map import Map
from player import Player

if __name__ == "__main__":
    print("Wilderness Survival System")

    map = Map(16, 32)
    player = Player("X")

    gold_bonus = GoldBonus(4)
    food_bonus = FoodBonus(4)
    water_bonus = WaterBonus(4)
    trader = Trader(4)

    map.add_player((2, 3), player)
    map.add_item((1, 2), gold_bonus)
    map.add_item((2, 2), food_bonus)
    map.add_item((3, 2), water_bonus)
    map.add_item((4, 2), trader)
    
    map.draw()
