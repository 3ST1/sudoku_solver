from src.DeductionRules.DeductionRule import DeductionRule
from src.SudokuGrid import SudokuGrid


class DR5(DeductionRule):
    def __init__(self, d: int = None) -> None:
        self.name = "X Wing"
        self.difficulty = d or 3

    def _apply_rule(self, grid: SudokuGrid):
        self.apply_x_wing(grid)

    def apply_x_wing(self, grid: SudokuGrid):
        raise NotImplementedError("I haven't finished to implement this rule yet")
