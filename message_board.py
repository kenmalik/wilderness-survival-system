from rich.text import Text
from direction import direction_strings


class MessageBoard():
    def __init__(self):
        self.message_stack: list[str] = []

    def on_event(self, event):
        if event.type == "moved":
            player = event.data["player"]
            direction = event.data["direction"]
            self.message_stack.append(f"Player {player.icon} moved {direction_strings[direction]}")

        if event.type == "item_picked_up":
            player = event.data["player"]
            item = event.data["item"]
            self.message_stack.append(f"Player {player.icon} picked up {item.icon}")
            
    def render(self) -> Text:
        display = Text()
        for message in reversed(self.message_stack):
            display.append(f"{message}\n")
        return display
