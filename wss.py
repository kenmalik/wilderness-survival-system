from direction import Direction
from map import Map
from message_board import MessageBoard
from player import Player
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
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


def get_player_stat_panels(players: list[Player]):
    panels: list[Panel] = []
    for player in players:
        panels.append(Panel(player.print_stats(), title=f"Player {player.icon} Stats"))
    return panels


if __name__ == "__main__":
    difficulty = Prompt.ask(
        "Enter preferred difficulty",
        choices=["Easy", "Medium", "Hard"],
        default="Hard",
        case_sensitive=False,
    )
    player_count = int(
        IntPrompt.ask(
            "How many players?",
            choices=["1", "2", "3", "4"],
            default="2",
        )
    )

    size = difficulty_presets[difficulty]["Size"]
    items = difficulty_presets[difficulty]["Items"]

    map = Map(size[0], size[1], items)

    players: list[Player] = []
    for i in range(1, player_count + 1):
        players.append(Player(str(i), map))
    map.place_players(players)

    messages = MessageBoard()

    map.register_listener(messages)

    layout = Layout()
    layout.split_column(
        Layout(map.draw(), name="map"),
        Layout(name="info"),
    )

    layout["info"].split_row(
        Layout(Panel("", title="Messages"), name="messages"),
        Layout(name="stats"),
    )

    layout["info"]["stats"].split_row(*get_player_stat_panels(players))
    layout["map"].ratio = 4

    with Live(layout, refresh_per_second=5, screen=True) as live:
        for _ in range(25):
            time.sleep(0.5)

            # map.populate_items(items)
            # map.generate_terrain(size[0], size[1])
            for player in players:
                player.move_direction(Direction.EAST)
            map.update()

            layout["map"].update(map.draw())
            layout["info"]["messages"].update(
                Panel(messages.render(), title="Messages")
            )
            layout["info"]["stats"].split_row(*get_player_stat_panels(players))
            live.update(layout)
