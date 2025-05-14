from abc import ABC, abstractmethod
from player import Player
from text_renderable import TextRenderable
from rich.text import Text
from event import Event
from message_board import MessageBoard
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
    
    

    def __init__(self):
        self.num_trades = 0
        self.MAX_TRADES = 0
        

    
            
    def trader_trade(self, player:Player):
        pass
    
    def player_trade( player:Player):
        pass
        
        
    def trade(self, player_modifier: int, trader_modifier: int) -> bool:
        player_roll = random.randint(1,20) + player_modifier
        trader_roll = random.randint(1,20) + trader_modifier
        return player_roll >= trader_roll
    
    def apply_effect(self, player: Player):
        while(self.num_trades <= self.MAX_TRADES):
            self.trader_trade(player)
            if(self.num_trades <= self.MAX_TRADES):
                self.player_trade(player)
            
            

    def render(self, context: Text):
        context.append(self.icon, style="white on black")
        
    
class FairTrader(Trader):
    def __init__(self):
        super().__init__()
        self.MAX_TRADES = 6
        
        
        
    def trader_trade(self, player: Player):
        give, take = random.sample(["gold", "water", "food"], 2)
        num_traded = random.randint(5, 15)
        #event offer
        
        #Trader giving gold
        if(give == "gold" ):
            if(take == "water"):
                if(num_traded >= player.current_water):
                    if(self.trade(num_traded*-1, 0)):
                        player.current_gold = player.current_gold + num_traded 
                        player.current_water = player.current_water - num_traded
                        self.num_trades+= 1
                        #accept
                    else:
                        #decline
                        self.num_trades+= 1
            elif(take == "food"):
                if(num_traded >= player.current_food):
                    if(self.trade(num_traded*-1, 0)):
                        player.current_gold = player.current_gold + num_traded
                        player.current_food = player.current_food - num_traded
                        self.num_trades+= 1
                        #accept
                    else:
                        #decline
                        self.num_trades+= 1
        
        #Trader giving water
        elif(give == "water"):
            if(take == "food"):
                if(num_traded >= player.current_food and player.current_food > player.current_water*2):
                    if(self.trade(0, 0)):
                        player.current_water = min(
                            player.current_water + num_traded, Player.MAX_WATER
                        )
                        player.current_food = player.current_food - num_traded
                        self.num_trades+= 1
                        #accept
                    else:
                        #decline
                        self.num_trades+= 1
            elif(take == "gold"):
                if(num_traded >= player.current_gold):
                    if(self.trade(0, 0)):
                        player.current_water = min(
                            player.current_water + num_traded, Player.MAX_WATER
                        )
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
        
        #Trader giving food
        elif(give == "food"):
            if(take == "water"):
                if(num_traded >= player.current_water and player.current_water > player.current_food*2):
                    if(self.trade(0, 0)):
                        player.current_food = min(
                            player.current_food + num_traded, Player.MAX_FOOD
                        )
                        player.current_water = player.current_water - num_traded
                        self.num_trades+= 1
                        self.messages.on_event(Event("player_dead", {"player": player}))
                    else:
                        #decline
                        self.num_trades+= 1
            elif(take == "gold"):
                if(num_traded >= player.current_gold):
                    if(self.trade(0, 0)):
                        player.current_food = min(
                            player.current_food + num_traded, Player.MAX_FOOD
                        )
                        player.current_gold = player.current_gold - num_traded
                        self.num_trades+= 1
                    else:
                        #decline
                        self.num_trades+= 1
                        
    def player_trade(self, player: Player):
        if(player.current_gold == 0):
            return
        num_traded = min(player.current_gold, random.randint(5, 15))
        if(player.current_food < player.current_water):
            if(self.trade(0,0)):
                player.current_water = min(
                    player.current_food + num_traded, Player.MAX_FOOD
                )
                player.current_gold = player.current_gold - num_traded
                self.num_trades += 1
                #accept
            else:
                self.num_trades += 1
                #decline
        else:
            if(self.trade(0,0)):
                player.current_water = min(
                    player.current_water + num_traded, Player.MAX_WATER
                )
                player.current_gold = player.current_gold - num_traded
                self.num_trades += 1
                #accept
            else:
                self.num_trades += 1
                #decline
            
        
                
        

    

        
    
    
        