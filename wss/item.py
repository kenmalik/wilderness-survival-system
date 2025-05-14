from abc import ABC, abstractmethod
from player import Player
from text_renderable import TextRenderable
from rich.text import Text
from event import Event
import random

class Item(TextRenderable, ABC):
    @abstractmethod
    def apply_effect(self, player: Player):
        pass


class GoldBonus(Item):
    icon = "G"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_gold += self.amount

    def render(self, context: Text):
        context.append(self.icon, style="bold black on yellow")


class FoodBonus(Item):
    icon = "F"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_food = min(
            player.current_food + self.amount, Player.MAX_FOOD
        )

    def render(self, context: Text):
        context.append(self.icon, style="bold white on dark_red")


class WaterBonus(Item):
    icon = "W"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_water = min(
            player.current_water + self.amount, Player.MAX_WATER
        )

    def render(self, context: Text):
        context.append(self.icon, style="bold white on dodger_blue3")


class Trader(Item):
    icon = "T"

    def __init__(self, amount: int):
        self.amount = amount

    def apply_effect(self, player: Player):
        player.current_water = min(
            player.current_water + self.amount, Player.MAX_WATER
        )
        player.current_food = min(
            player.current_food + self.amount, Player.MAX_FOOD
        )
        
    def trade(self, player_modifier: int, trader_modifier: int) -> bool:
        player_roll = random.randint(1,20) + player_modifier
        trader_roll = random.randint(1,20) + trader_modifier
        return player_roll >= trader_roll

    def render(self, context: Text):
        context.append(self.icon, style="white on black")
        
    
class FairTrader(Trader):
    def __init__(self):
        super().__init__(0)
        self.num_trades = 0
        
        
    def trader_trade(self, player: Player):
        give, take = random.sample(["gold", "water", "food"], 2)
        num_traded = random.randint(5, 15)
        #Trader giving gold
        if(give == "gold" ):
            if(take == "water"):
                if(num_traded >= player.current_water):
                    if(super.trade(num_traded*-1, 0)):
                        #event stuff
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
            elif(take == "food"):
                if(num_traded >= player.current_):
                    if(self.trade(num_traded*-1, 0)):
                        #event stuff
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
        #Trader giving water
        if(give == "water"):
            if(take == "food"):
                if(num_traded >= player.current_food and player.current_food > player.current_water*2):
                    if(self.trade(0, 0)):
                        #event stuff
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
            elif(take== "gold"):
                if(num_traded >= player.current_gold):
                    if(self.trade(0, 0)):
                        #event stuff
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
        #Trader giving food
        if(give == "food"):
            if(take == "water"):
                if(num_traded >= player.current_water and player.current_water > player.current_food*2):
                    if(self.trade(0, 0)):
                        #event stuff
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
            elif(take == "gold"):
                if(num_traded >= player.current_gold):
                    if(super.trade(0, 0)):
                        #event stuff
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
                        
        
                
        

    

        
    
    
        