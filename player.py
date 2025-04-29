from text_renderable import TextRenderable
from rich.text import Text


class Player(TextRenderable):
    def __init__(self, icon: str):
        self.current_strength = 0
        self.current_water = 0
        self.current_food = 0
        self.current_gold = 0
        self.icon = icon

    def print_stats(self):
        print(
            f"""Strength: {self.current_strength}
              Water: {self.current_water}
              Food: {self.current_food}
              Gold: {self.current_gold}"""
        )

    def render(self, context: Text):
        context.append(self.icon, style="bold white on indian_red")
