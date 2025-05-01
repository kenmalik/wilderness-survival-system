class Event:
    def __init__(self, type: str, data: dict):
        self.type: str = type
        self.data: dict = data or {}
