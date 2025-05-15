"""
Event module for the Wilderness Survival System.
This module defines the Event class used for game event handling and communication
between different components of the system.
"""

class Event:
    """
    Represents a game event that can be passed between components.
    Events are used to communicate state changes and actions throughout the game.
    
    Attributes:
        type (str): The type of event (e.g., "moved", "item_picked_up", "player_dead")
        data (dict): Additional data associated with the event
    """
    def __init__(self, type: str, data: dict | None):
        """
        Initialize a new event.
        
        Args:
            type (str): The type of event
            data (dict): Additional data for the event, defaults to empty dict if None
        """
        self.type: str = type
        self.data: dict = data or {}
