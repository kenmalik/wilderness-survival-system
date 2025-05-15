from abc import ABC, abstractmethod
from rich.text import Text

class TextRenderable(ABC):
    @abstractmethod
    def render(self, context: Text):
        pass
