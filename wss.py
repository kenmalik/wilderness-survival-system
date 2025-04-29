from item import Trader
from map import Map
from player import Player
from console import console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
import time

if __name__ == "__main__":
    map = Map(32, 128)
    player = Player("P")

    trader = Trader(4)

    map.add_player((2, 3), player)
    map.populate_items()
    map.add_item((4, 2), trader)

    layout = Layout()
    layout.split_column(
        Layout(map.draw(), name="map"),
        Layout(Panel("Messages here", title="Messages"), name="messages"),
    )
    layout["map"].ratio = 4

    with Live(layout, refresh_per_second=4, screen=True) as live:
        for _ in range(25):
            time.sleep(0.4)
            map.populate_items()
            layout["map"].update(map.draw())
            live.update(layout)
