# ./src/DeductionRule.py
from src.SudokuGrid import SudokuGrid


class DeductionRule:
    """
    Base class for all deduction rules.
    This class should not be instantiated directly but should be subclassed.
    It provides a common template for all deduction rules.

    Attributes:
    name: str: The name of the deduction rule.
    difficulty: int: The difficulty level of the deduction rule.
    has_changed: bool: A flag to indicate whether the rule has made any changes to the grid.

    Methods:
    get_name(): Returns the name of the deduction rule.
    get_difficulty(): Returns the difficulty level of the deduction rule.
    apply_rule(grid: SudokuGrid, verbose: bool): Applies the deduction rule to the grid (through the _apply_rule method) and returns a boolean indicating whether the rule has made any changes to the grid.
    _apply_rule(grid: SudokuGrid): Applies the deduction rule to the grid. This method should be implemented by subclasses.
    """

    name: str = NotImplementedError("Subclasses should set name at initialization.")
    difficulty: int = NotImplementedError(
        "Subclasses should set difficulty at initialization."
    )
    has_changed: bool = False

    def get_name(self) -> str:
        return self.name

    def get_difficulty(self) -> int:
        return self.difficulty

    def apply_rule(self, grid: SudokuGrid, verbose=False) -> bool:
        self.has_changed = False
        if verbose:
            print(f"USING DR{self.get_difficulty()}: {self.get_name()}")
        self._apply_rule(grid)
        # print(f"DEBUG has_changed after applying {self.get_name()}: {self.has_changed}")
        return self.has_changed

    def _apply_rule(self, grid: SudokuGrid):
        raise NotImplementedError(
            "Subclasses should implement _apply_rule(self, grid)."
        )
