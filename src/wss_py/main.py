import sys
import logging
import signal

from rich.prompt import IntPrompt, Prompt
from rich.columns import Columns
from rich.panel import Panel
from rich import print

from wss_py.game import Game
from wss_py.vision import Vision, FocusedVision, CautiousVision, KeenEyedVision, FarSightVision
from wss_py.brain import Brain, FoodBrain, WaterBrain, GoldBrain

logger = logging.getLogger(__name__)


def signal_handler(signum, _):
    logger.info(f"Received signal {signum}, exiting.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def get_vision_type(player_num: int) -> Vision:
    vision_choices = {
        "1": "Focused Vision - Sees forward and diagonally",
        "2": "Cautious Vision - Sees forward and to the sides",
        "3": "Keen-Eyed Vision - Sees wider area forward",
        "4": "Far-Sight Vision - Sees the furthest ahead",
    }

    print(f"\n[bold]Vision types for Player {player_num}:")
    for key, desc in vision_choices.items():
        print(f"{key}. {desc}")

    choice = Prompt.ask(
        f"Select vision type for Player {player_num}",
        choices=["1", "2", "3", "4"],
        default="1",
    )

    vision_map = {
        "1": FocusedVision,
        "2": CautiousVision,
        "3": KeenEyedVision,
        "4": FarSightVision,
    }

    return vision_map[choice]()


def get_brain_type(player_num: int) -> Brain:
    brain_choices = {
        "1": "Food Brain - Prioritizes finding food",
        "2": "Water Brain - Prioritizes finding water",
        "3": "Gold Brain - Prioritizes finding gold",
    }

    print(f"\n[bold]Brain types for Player {player_num}:")
    for key, desc in brain_choices.items():
        print(f"{key}. {desc}")

    choice = Prompt.ask(
        f"Select brain type for Player {player_num}",
        choices=["1", "2", "3"],
        default="1",
    )

    brain_map = {"1": FoodBrain, "2": WaterBrain, "3": GoldBrain}

    return brain_map[choice]

def get_difficulty() -> str:
    difficulty_choices = {
        "1": "Easy",
        "2": "Medium",
        "3": "Hard",
    }

    print("[bold]Difficulty levels:")
    for key, desc in difficulty_choices.items():
        print(f"{key}. {desc}")

    choice = Prompt.ask(
        "Select difficulty level",
        choices=["1", "2", "3"],
        default="2",
    )

    return difficulty_choices[choice]

def get_default_configs(player_count: int) -> list[dict]:
    """
    Get default configurations for players based on the number of players.
    
    Args:
        player_count (int): Number of players in the game.
        
    Returns:
        list[dict]: List of dictionaries containing default configurations for each player.
    """
    default_configs: list[dict] = []
    for _ in range(1, player_count + 1):
        default_configs.append({
            "vision": FocusedVision(),
            "brain": FoodBrain,
        })
    return default_configs

def confirm_configuration(player_configs: list[dict]) -> bool:
    """
    Confirm the player configurations with the user.
    
    Args:
        player_configs (list[dict]): List of player configurations to confirm.
        
    Returns:
        bool: True if the configuration is confirmed, False otherwise.
    """
    print("\n[bold]Current player configurations:")
    config_display = [ Panel(f"{config['vision']}\n{config['brain'].__name__}", title=f"Player {i+1}") for i, config in enumerate(player_configs) ]
    print(Columns(config_display, equal=True))
    return Prompt.ask("Is this configuration okay?", choices=["y", "n"], default="y") == "y"

def main():
    logging.basicConfig(filename="wss.log", level=logging.DEBUG)
    logger.info("Started")

    difficulty = get_difficulty()
    player_count = int(
        IntPrompt.ask(
            "\nHow many players?",
            choices=["1", "2", "3", "4"],
            default="2",
        )
    )

    # Get player customizations
    player_configs = get_default_configs(player_count)
    config_ok = confirm_configuration(player_configs)

    while not config_ok:
        for i in range(player_count):
            player_configs[i]["vision"] = get_vision_type(i + 1)
            player_configs[i]["brain"] = get_brain_type(i + 1)
        config_ok = confirm_configuration(player_configs)

    game = Game(difficulty, player_count, player_configs)
    game.run()

    logger.info("Finished")


if __name__ == "__main__":
    main()
