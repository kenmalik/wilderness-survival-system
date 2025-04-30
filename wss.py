from direction import Direction
from map import Map
from message_board import MessageBoard
from player import Player
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
import time
import random

difficulty_presets = {
    "Easy": {
        "Size": (16, 64),
        "Items": 10,
    },
    "Medium": {
        "Size": (24, 96),
        "Items": 15,
    },
    "Hard": {
        "Size": (32, 128),
        "Items": 20,
    },
}

if __name__ == "__main__":
    difficulty = Prompt.ask(
        "Enter preferred difficulty",
        choices=["Easy", "Medium", "Hard"],
        default="Hard",
        case_sensitive=False,
    )

    size = difficulty_presets[difficulty]["Size"]
    items = difficulty_presets[difficulty]["Items"]

    map = Map(size[0], size[1], items)
    player = Player("P", map)
    player.print_stats()

    messages = MessageBoard()

    map.register_listener(messages)
    map.add_player((random.randrange(0, size[0]), 0), player)

    layout = Layout()
    layout.split_column(
        Layout(map.draw(), name="map"),
        Layout(name="info"),
    )
    layout["info"].split_row(
        Layout(Panel("", title="Messages"), name="messages"), 
        Layout(Panel.fit(player.print_stats(), title=f"Player {player.icon} Stats"), name="stats"), 
    )
    layout["map"].ratio = 4

    with Live(layout, refresh_per_second=5, screen=True) as live:
        for _ in range(25):
            time.sleep(0.5)

            # map.populate_items(items)
            # map.generate_terrain(size[0], size[1])
            player.move_direction(Direction.EAST)
            map.update()

            layout["map"].update(map.draw())
            layout["info"]["messages"].update(Panel(messages.render(), title="Messages"))
            layout["info"]["stats"].update(Panel.fit(player.print_stats(), title=f"Player {player.icon} Stats"))
            live.update(layout)
