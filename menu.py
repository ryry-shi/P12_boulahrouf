from typing import Callable, Iterable, Tuple
from utils import ask_user_choice, clear_screen


class Menu:
    
    def __init__(self, title: str, choices: Iterable[Tuple[str, Callable]]) -> None:
        self.title = title
        self.choices = choices

    def _draw(self) -> None:
        for k, (choice, _) in enumerate(self.choices):
            print(f"{k + 1}: {choice}")

    def run(self) -> None:
        clear_screen()
        print(f".: {self.title} :.")
        self._draw()
        choice_nb = ask_user_choice(len(self.choices))
        _, on_choice = self.choices[choice_nb]
        on_choice()
