from message_board import MessageBoard
from map import Map
from player import Player
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from player import Player
from event import Event

from vision import FocusedVision

import time


class Game:
    difficulty_presets = {
        "Easy": {
            "map_size": (16, 64),
            "item_count": 30,
        },
        "Medium": {
            "map_size": (24, 96),
            "item_count": 80,
        },
        "Hard": {
            "map_size": (32, 128),
            "item_count": 100,
        },
    }

    def __init__(self, difficulty: str, player_count: int, player_configs: list[dict] | None = None):
        self.game_over = False

        map_size = self.difficulty_presets[difficulty]["map_size"]
        item_count = self.difficulty_presets[difficulty]["item_count"]
        self.map = Map(map_size[0], map_size[1], item_count, difficulty)

        self.dead_players: list[Player] = []
        self.players: list[Player] = []
        
        # Use default configurations if none provided
        if player_configs is None:
            player_configs = [{"vision": FocusedVision(), "brain": "food"} for _ in range(player_count)]
        
        for i in range(1, player_count + 1):
            config = player_configs[i-1]
            self.players.append(Player(str(i), self.map, config["vision"], config["brain"]))
            
        self.map.place_players(self.players)

        self.messages = MessageBoard()
        self.map.register_listener(self.messages)

        self.layout = Game.make_ui()
        self.update_ui()

    @classmethod
    def make_ui(cls):
        layout = Layout()
        layout.split_column(
            Layout(name="map"),
            Layout(name="info"),
        )
        layout["map"].ratio = 4
        layout["info"].split_row(
            Layout(name="messages"),
            Layout(name="stats"),
        )
        layout["info"]["stats"].ratio = 2
        return layout

    @classmethod
    def get_player_stat_panels(cls, players: list[Player]):
        panels: list[Panel] = []
        for player in players:
            title = f"Player {player.icon}"

            if player.dead:
                title += " (Dead)"
            else:
                title += " Stats"

            panels.append(
                Panel(player.print_stats(), title=title)
            )
        return panels

    def update_ui(self) -> None:
        self.layout["map"].update(self.map.draw())
        self.layout["info"]["messages"].update(
            Panel(self.messages.render(), title="Messages")
        )
        self.layout["info"]["stats"].split_row(
            *Game.get_player_stat_panels(self.players)
        )

    def run(self) -> None:
        with Live(self.layout, refresh_per_second=60, screen=True) as live:
            while not self.game_over:
                for player in self.players:
                    time.sleep(0.15)
                    if player.dead:
                        continue

                    player.update()

                    if player.x == len(self.map.terrain[0]) - 1:
                        self.game_over = True

                    if (
                        player.current_strength <= 0
                        or player.current_food <= 0
                        or player.current_water <= 0
                    ):
                        self.messages.on_event(Event("player_dead", {"player": player}))
                        self.dead_players.append(player)
                        player.dead = True

                    self.update_ui()
                    live.update(self.layout)

                if len(self.dead_players) == len(self.players):
                    self.game_over = True

            while True: # Keep display up after game ends until interrupt
                pass

    def demo_terrain(self) -> None:
        preset = self.difficulty_presets["Hard"]
        with Live(self.layout, refresh_per_second=5, screen=True) as live:
            for _ in range(25):
                time.sleep(0.5)

                self.map.populate_items(preset["item_count"])
                self.map.generate_terrain(preset["map_size"][0], preset["map_size"][1])
                for player in self.players:
                    player.update()

                self.update_ui()
                live.update(self.layout)
