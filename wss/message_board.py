from rich.text import Text
from direction import direction_strings
from listener import Listener
from event import Event


class MessageBoard(Listener):
    def __init__(self):
        self.message_stack: list[str] = []

    def on_event(self, event: Event) -> None:
        if event.type == "moved":
            player = event.data["player"]
            direction = event.data["direction"]
            self.message_stack.append(f"Player {player.icon}: I'll travel {direction_strings[direction]}")

        if event.type == "item_picked_up":
            player = event.data["player"]
            item = event.data["item"]
            self.message_stack.append(f"Player {player.icon}: picked up some {item.icon}")

        if event.type == "terrain_entered":
            player = event.data["player"]
            new_terrain = event.data["new_terrain"]
            self.message_stack.append(f"Player {player.icon}: at a {new_terrain}")

        if event.type == "game_won":
            player = event.data["player"]
            self.message_stack.append(f"Player {player.icon} wins!")

        if event.type == "player_dead":
            player = event.data["player"]
            self.message_stack.append(f"Player {player.icon} died!")
            
        if event.type == "trade_accepted":
            player = event.data["player"]
            self.message_stack.append(f"Player {player.icon}: traded with the trader!")
            
        if event.type == "trade_accepted":
            player = event.data["player"]
            self.message_stack.append(f"Player {player.icon}: failed to trade with the trader!")
        
        if event.type == "trader_offer":
            player = event.data["player"]
            item_given = event.data["item_given"]
            item_received = event.data["item_received"]
            self.message_stack.append(f"Player {player.icon}: The Trader offers your {item_given.icon} for their {item_received.icon}")
            
        if event.type == "player_offer":
            player = event.data["player"]
            item_given = event.data["item_given"]
            item_received = event.data["item_received"]
            self.message_stack.append(f"Player {player.icon}: offered {item_given.icon} for the Traders {item_received.icon}")    
        
        if len(self.message_stack) > 10:
            self.message_stack = self.message_stack[-10:]

    def render(self) -> Text:
        display = Text()
        for message in reversed(self.message_stack):
            display.append(f"{message}\n")
        return display
