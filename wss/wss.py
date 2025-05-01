import sys
from rich.prompt import IntPrompt, Prompt

from game import Game

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

    game = Game(difficulty, player_count)

    if len(sys.argv) > 1 and sys.argv[1] == "--demo-terrain":
        game.demo_terrain()
    else:
        game.run()
