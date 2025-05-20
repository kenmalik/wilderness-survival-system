"""
Main game module for the Wilderness Survival System.
This module handles the core game logic, including game state, player management,
and UI rendering.
"""

from wss_py.message_board import MessageBoard
from wss_py.map import Map
from wss_py.player import Player
from wss_py.event import Event

from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.align import Align

import time


class Game:
    """
    Main game class that manages the game state, players, and UI.
    
    The game is a wilderness survival simulation where players must navigate
    through terrain, manage resources, and survive until reaching the end.
    """
    
    # Predefined difficulty levels with corresponding map sizes and item counts
    difficulty_presets = {
        "Easy": {
            "map_size": (16, 64),    # Height: 16, Width: 64
            "item_count": 80,        # Number of items to spawn
        },
        "Medium": {
            "map_size": (24, 96),    # Height: 24, Width: 96
            "item_count": 120,       # Number of items to spawn
        },
        "Hard": {
            "map_size": (32, 128),   # Height: 32, Width: 128
            "item_count": 200,       # Number of items to spawn
        },
    }

    def __init__(self, difficulty: str, player_count: int, player_configs: list[dict]):
        """
        Initialize a new game instance.
        
        Args:
            difficulty (str): Game difficulty level ("Easy", "Medium", "Hard")
            player_count (int): Number of players in the game
            player_configs (list[dict], optional): Custom player configurations
        """
        self.game_over = False

        # Initialize map based on difficulty settings
        map_size = self.difficulty_presets[difficulty]["map_size"]
        item_count = self.difficulty_presets[difficulty]["item_count"]
        self.map = Map(map_size[0], map_size[1], item_count, difficulty)

        # Initialize player lists
        self.dead_players: list[Player] = []
        self.players: list[Player] = []
        
        # Create players with their configurations
        for i in range(1, player_count + 1):
            config = player_configs[i-1]
            player = Player(str(i), self.map, config["vision"])
            player.set_brain(config["brain"](player))
            self.players.append(player)
            
        self.map.place_players(self.players)

        # Initialize message board and UI
        self.messages = MessageBoard()
        self.map.register_listener(self.messages)

        self.layout = Game.make_ui()
        self.update_ui()

    @classmethod
    def make_ui(cls):
        """
        Create the game's UI layout using Rich library.
        
        Returns:
            Layout: A Rich layout object containing the game's UI structure
        """
        layout = Layout()
        layout.split_column(
            Layout(name="map"),      # Main game map
            Layout(name="info"),     # Information panel
        )
        layout["map"].ratio = 4
        layout["info"].split_row(
            Layout(name="messages"), # Message display
            Layout(name="stats"),    # Player statistics
        )
        layout["info"]["stats"].ratio = 2
        return layout

    @classmethod
    def get_player_stat_panels(cls, players: list[Player]):
        """
        Generate Rich panels displaying player statistics.
        
        Args:
            players (list[Player]): List of players to generate stats for
            
        Returns:
            list[Panel]: List of Rich panels containing player statistics
        """
        panels: list[Panel] = []
        for player in players:
            title = f"Player {player.icon}"

            if player.dead:
                title += " (Dead)"
            else:
                title += " Stats"

            panels.append(
                Panel(player.print_stats(), title=title, border_style="grey53" if player.dead else "none")
            )
        return panels

    def update_ui(self) -> None:
        """
        Update all UI components with current game state.
        """
        self.layout["map"].update(self.map.draw())
        self.layout["info"]["messages"].update(
            Panel(self.messages.render(), title="Messages")
        )
        self.layout["info"]["stats"].split_row(
            *Game.get_player_stat_panels(self.players)
        )

    def run(self) -> None:
        """
        Main game loop. Handles player turns, game state updates, and UI rendering.
        Game continues until all players are dead or a player reaches the end.
        """
        with Live(self.layout, refresh_per_second=30, screen=True) as live:
            winner = None

            while not self.game_over:
                for player in self.players:
                    time.sleep(0.1)  # Add slight delay between player turns
                    if player.dead:
                        continue

                    player.update()

                    # Check if player reached the end
                    if player.x == len(self.map.terrain[0]) - 1:
                        self.game_over = True
                        winner = player

                    # Check if player died from resource depletion
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

                # Check if all players are dead
                if len(self.dead_players) == len(self.players):
                    self.game_over = True

            if winner:
                message = Text(f"Player {winner.icon} wins!", style="bold green")
            else:
                message = Text("All players are dead!", style="bold red")

            message_visible = True
            while True:
                live.update(Layout(Panel(Align(message, align="center", vertical="middle") if message_visible else "", title="Game Over")))
                time.sleep(0.8)
                message_visible = not message_visible
