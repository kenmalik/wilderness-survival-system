from abc import ABC, abstractmethod

from event import Event

class Listener(ABC):
    @abstractmethod
    def on_event(self, event: Event) -> None:
        pass
