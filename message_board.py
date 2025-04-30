from rich.text import Text
from direction import direction_strings


class MessageBoard():
    def __init__(self):
        self.message_stack: list[str] = []

    def on_event(self, event):
        if event.type == "moved":
            player = event.data["player"]
            direction = event.data["direction"]
            self.message_stack.append(f"Player {player.icon}: I'll travel {direction_strings[direction]}")

        if event.type == "item_picked_up":
            player = event.data["player"]
            item = event.data["item"]
            self.message_stack.append(f"Player {player.icon}: picked up some {item.icon}")

        if event.type == "environment_entered":
            player = event.data["player"]
            new_environment = event.data["new_environment"]
            self.message_stack.append(f"Player {player.icon}: at a {new_environment}")
            
    def render(self) -> Text:
        display = Text()
        for message in reversed(self.message_stack):
            display.append(f"{message}\n")
        return display
