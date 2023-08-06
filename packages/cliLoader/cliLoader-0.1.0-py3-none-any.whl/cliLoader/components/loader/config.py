class Config:
    COLORS = {
        "BLACK": 30, "RED": 31, "GREEN": 32,
        "YELLOW": 33, "BLUE": 34, "PURPLE": 35,
        "CYAN": 36, "WHITE": 37
    }
    def __init__(self, **kwargs):
        self.width: int = kwargs.get('width', 0)
        self.progress_char: int = kwargs.get("progress_char", "█")
        self.color: int = kwargs.get("color", __class__.COLORS["WHITE"])
        self.destination: int = kwargs.get("destination", 0)
        self.border: str = kwargs.get("border", "|")


Config = Config
