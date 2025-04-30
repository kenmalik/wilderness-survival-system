from message_board import MessageBoard
from map import Map
from player import Player
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from direction import Direction
from player import Player

import time


class Game:
    difficulty_presets = {
        "Easy": {
            "map_size": (16, 64),
            "item_count": 10,
        },
        "Medium": {
            "map_size": (24, 96),
            "item_count": 15,
        },
        "Hard": {
            "map_size": (32, 128),
            "item_count": 20,
        },
    }

    def __init__(self, difficulty: str, player_count: int):
        map_size = self.difficulty_presets[difficulty]["map_size"]
        item_count = self.difficulty_presets[difficulty]["item_count"]

        self.map = Map(map_size[0], map_size[1], item_count)

        self.players: list[Player] = []
        for i in range(1, player_count + 1):
            self.players.append(Player(str(i), self.map))
        self.map.place_players(self.players)

        self.messages = MessageBoard()

        self.map.register_listener(self.messages)

        self.layout = Layout()
        self.layout.split_column(
            Layout(self.map.draw(), name="map"),
            Layout(name="info"),
        )

        self.layout["info"].split_row(
            Layout(Panel("", title="Messages"), name="messages"),
            Layout(name="stats"),
        )

        self.layout["info"]["stats"].split_row(
            *Game.get_player_stat_panels(self.players)
        )
        self.layout["map"].ratio = 4

    @classmethod
    def get_player_stat_panels(cls, players: list[Player]):
        panels: list[Panel] = []
        for player in players:
            panels.append(
                Panel(player.print_stats(), title=f"Player {player.icon} Stats")
            )
        return panels

    def run(self) -> None:
        with Live(self.layout, refresh_per_second=5, screen=True) as live:
            for _ in range(25):
                time.sleep(0.5)

                # map.populate_items(items)
                # map.generate_terrain(size[0], size[1])
                for player in self.players:
                    player.move_direction(Direction.EAST)
                self.map.update()

                self.layout["map"].update(self.map.draw())
                self.layout["info"]["messages"].update(
                    Panel(self.messages.render(), title="Messages")
                )
                self.layout["info"]["stats"].split_row(
                    *Game.get_player_stat_panels(self.players)
                )
                live.update(self.layout)
