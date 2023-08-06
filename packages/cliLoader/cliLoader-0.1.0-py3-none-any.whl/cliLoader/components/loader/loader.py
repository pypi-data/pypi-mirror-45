import os
from .config import Config


class _Loader:
    def __init__(self, config):
        self.config: Config = config
        self._counter: int = 0
        self._percentage: int = 0
        self._part: int = 0

    @property
    def completed(self):
        return self._counter

    @completed.setter
    def completed(self, c):
        self._counter = c

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, p):
        counter, destination = p
        p = int((counter / destination) * 100)
        self._percentage = p

    def set_percentage(self):
        self.percentage = (self.completed, self.config.destination)

    @property
    def part(self):
        return self._part

    @part.setter
    def part(self, p):
        width, percentage = p
        p = int(width * (percentage/100))
        self._part = p

    def set_part(self):
        self.part = (self.config.width, self.percentage)

    def set_progress_bar(self):
        progress = (self.config.progress_char * self.part + " " * (self.config.width - self.part))
        return f" {self.config.border}{progress}{self.config.border}{self.percentage}%"

    def show(self, info_text="", completed=0):
        self.set_percentage()
        self.set_part()
        self.clear()
        self.print_state(info_text)
        self.completed += completed

    def print_state(self, text):
        end_color = '\033[m'  # reset to the defaults
        color = f'\033[{self.config.color}m'  # Green Text
        print(text+color + self.set_progress_bar(), end_color)

    def clear(self):
        # for windows
        try:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
        except KeyboardInterrupt:
            # quit
            exit()



Loader = _Loader
