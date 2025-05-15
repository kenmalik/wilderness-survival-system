import sys
from rich.prompt import IntPrompt, Prompt
import logging
import signal

from game import Game
from vision import Vision, FocusedVision, CautiousVision, KeenEyedVision, FarSightVision
from brain import FoodBrain, WaterBrain, GoldBrain

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

    print(f"\nVision types for Player {player_num}:")
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


def get_brain_type(player_num: int) -> str:
    brain_choices = {
        "1": "Food Brain - Prioritizes finding food",
        "2": "Water Brain - Prioritizes finding water",
        "3": "Gold Brain - Prioritizes finding gold",
    }

    print(f"\nBrain types for Player {player_num}:")
    for key, desc in brain_choices.items():
        print(f"{key}. {desc}")

    choice = Prompt.ask(
        f"Select brain type for Player {player_num}",
        choices=["1", "2", "3"],
        default="1",
    )

    brain_map = {"1": FoodBrain, "2": WaterBrain, "3": GoldBrain}

    return brain_map[choice]


def main():
    logging.basicConfig(filename="wss.log", level=logging.DEBUG)
    logger.info("Started")

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

    # Get player customizations
    player_configs = []
    for i in range(1, player_count + 1):
        vision = get_vision_type(i)
        brain = get_brain_type(i)
        player_configs.append({"vision": vision, "brain": brain})

    game = Game(difficulty, player_count, player_configs)

    if len(sys.argv) > 1 and sys.argv[1] == "--demo-terrain":
        game.demo_terrain()
    else:
        game.run()

    logger.info("Finished")


if __name__ == "__main__":
    main()
