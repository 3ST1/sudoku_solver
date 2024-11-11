from src.DeductionRules.DeductionRule import DeductionRule
from src.SudokuGrid import SudokuGrid


class DR7(DeductionRule):
    def __init__(self, d: int = None) -> None:
        self.name = "Swordfish"
        self.difficulty = d or 3

    def _apply_rule(self, grid: SudokuGrid):
        return self.apply_swordfish(grid)

    def apply_swordfish(self, grid: SudokuGrid):
        raise NotImplementedError("I haven't finished to implement this rule yet")
