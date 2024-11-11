from src.DeductionRules.DeductionRule import DeductionRule
from src.SudokuGrid import Cell, SudokuGrid


class DR1(DeductionRule):
    """
    DR1 is a deduction rule base class for implementing Naked Strategies. It inherits from the DeductionRule base class.
    """

    def __init__(self, name: str, d: int) -> None:
        super().__init__()
        self.name = name
        self.difficulty = d

    def _apply_rule(self, grid: SudokuGrid):
        for unit in (grid.rows, grid.cols, grid.zones):
            if self._apply_naked_rule(unit):
                return  # to avoid applying the rule 3 times for naked singles

    def _apply_naked_rule(self, group: list[list[Cell]]):
        raise NotImplementedError("Subclasses must implement this method.")


class DR1_1(DR1):
    """
    DR1_1 is a subclass of DR1 that implements the "Naked Singles" strategy for solving sudoku puzzles.
    The "Naked Singles" strategy sets the value of a cell if there is only one possible value for that cell.
    This class provides a method to apply this strategy to a group of cells.
    """

    def __init__(self, d=None):
        super().__init__(name="Naked Singles", d=d or 1)

    def _apply_naked_rule(self, group: list[list[Cell]]):
        """
        Apply the naked single strategy to a group of cells.
        The naked single strategy sets the value of a cell if there is only one possible value for that cell.
        This method iterates through each cell in the provided group of cells and sets the cell's value if
        it meets the criteria of the naked single strategy.
        Args:
            group (list[list[Cell]]): A list of lists, where each inner list represents a group of cells
                                      (e.g., a row, column, or block in the sudoku grdi ).
        Returns:
            bool: returns True to indicate the rule has been applied and avoid applying the rule 3 times for grid.rows, grid.cols and grid.zones

        """
        for g in group:
            for cell in g:
                # If there is only one possible value for the cell -> set it
                if cell.val == -1 and len(cell.notes) == 1:
                    cell.set_value(cell.notes.pop())
                    self.has_changed = True

        # to avoid applying the rule 3 times for grid.rowws, grid.cols and grid.zones (grid.rows is enough)
        return True


class DR1_2(DR1):
    """
    DR1_2 is a subclass of DR1 that implements the "Naked Pair" deduction rule for solving sudoku puzzles.
    A naked pair is a pair of cells within a unit (row, column, or block) that both contain the same two candidate numbers.
    These pairs can be used to eliminate these two candidate numbers from the other cells in the unit.
    """

    def __init__(self, d=None):
        super().__init__(name="Naked Pair", d=d or 2)

    def find_naked_pairs(self, cells: list[Cell]) -> list[tuple[Cell, Cell]]:
        """
        Identifies naked pairs in a list of cells.
        A naked pair is a pair of cells within a unit (row, column, or block) that
        both contain the same two candidate numbers. These pairs can be used to
        eliminate these two candidate numbers from the other cells in the unit.
        Args:
            cells (list[Cell]): A list of Cell objects to search for naked pairs.
        Returns:
            list[tuple[Cell, Cell]]: A list of tuples, each containing two Cell
            objects that form a naked pair.
        """

        pairs = []
        candidate_cells = [cell for cell in cells if len(cell.notes) == 2]
        for cell in candidate_cells:
            for other_cell in candidate_cells:
                if cell != other_cell and cell.notes == other_cell.notes:
                    pairs.append((cell, other_cell))
        return pairs

    def _apply_naked_rule(self, group: list[list[Cell]]):
        """
        Applies the naked pair rule to a group of cells .
        The naked pair rule identifies pairs of cells within a group (row, column, or zone)
        that have the same two candidate notes. These pairs can be used to eliminate those
        candidate notes from other cells in the same group.
        Args:
            group (list[list[Cell]]): A list of lists of Cell objects representing a group
                                      of cells in the sudoku grid (e.g., a row, column, or zone).
        Raises:
            ValueError: If removing a note causes a cell to end up with an empty note set.
        """

        for g in group:
            # only empty cells (just in case)
            cells = [cell for cell in g if cell.val == -1]

            pairs = self.find_naked_pairs(cells)

            for cell1, cell2 in pairs:
                # Restrict candidate elimination to cells in the shared zone, row, or column
                related_cells = set(g)
                if cell1.row_idx == cell2.row_idx:
                    related_cells |= cell1.observer.row
                if cell1.col_idx == cell2.col_idx:
                    related_cells |= cell1.observer.col
                if cell1.zone_idx == cell2.zone_idx:
                    related_cells |= cell1.observer.zone

                related_cells: list[Cell] = [
                    cell
                    for cell in related_cells
                    if cell not in (cell1, cell2) and cell.val == -1
                ]

                # Remove the pair's notes from the related cells
                for cell in related_cells:
                    for note in cell1.notes:
                        if note in cell.notes:
                            cell.notes.remove(note)
                            self.has_changed = True

                            # Check if removing note caused an empty set
                            if not cell.notes:
                                raise ValueError(
                                    f"Error: Cell at ({cell.row_idx}, {cell.col_idx}) ended up with an empty note set."
                                )


class DR1_3(DR1):
    """
    DR1_3 is a subclass od DR1 class and implements the naked triples deduction rule for solving sudoku puzzles.
    A naked triple is a set of three cells within a unit (row, column, or block) that collectively contain exactly three unique candidates.
    These candidates can be used to eliminate other candidates from the same unit.

    """

    def __init__(self, d=None):
        super().__init__(name="Naked Triple", d=d or 2)

    def find_naked_triples(self, cells: list[Cell]) -> list[tuple[Cell, Cell, Cell]]:
        """
        Identifies all naked triples within a given list of cells.
        A naked triple is a set of three cells within a unit (row, column, or block)
        that collectively contain exactly three unique candidates. These candidates
        can be used to eliminate other candidates from the same unit.
        Args:
            cells (list[Cell]): A list of Cell objects to search for naked triples.
        Returns:
            list[tuple[Cell, Cell, Cell]]: A list of tuples, each containing three
            Cell objects that form a naked triple.
        """
        triples = []
        candidate_cells = [cell for cell in cells if 2 <= len(cell.notes) <= 3]  # *
        # *The combinations of candidates for a Naked Triple will be one of the following:
        # (123) (123) (123) - {3/3/3} (in terms of candidates per cell)
        # (123) (123) (12) - {3/3/2} (or some combination thereof)
        # (123) (12) (23) - {3/2/2}
        # (12) (23) (13) - {2/2/2}

        for cell in candidate_cells:
            for other_cell in candidate_cells:
                if cell != other_cell:
                    for third_cell in candidate_cells:
                        if third_cell != cell and third_cell != other_cell:
                            # Union of notes should be exactly three unique candidates
                            combined_notes = (
                                set(cell.notes)
                                | set(other_cell.notes)
                                | set(third_cell.notes)
                            )

                            # A naked triple should have exactly three unique notes values
                            if len(combined_notes) == 3:
                                # We should be able to create the pattern (1,2) (2,3) (1,3) with the notes of the cells
                                len_cells = sorted(
                                    [
                                        len(cell.notes),
                                        len(other_cell.notes),
                                        len(third_cell.notes),
                                    ]
                                )
                                # if lenghts are [2,3,3] or [3,3,3] then we are sure that we can create the pattern else we need to check
                                if len_cells == [2, 2, 3] or len_cells == [2, 2, 2]:
                                    if (
                                        not cell.notes
                                        != other_cell.notes
                                        != third_cell.notes
                                    ):
                                        continue

                                triples.append((cell, other_cell, third_cell))

        return triples

    def _apply_naked_rule(self, group: list[list[Cell]]):
        """
        Applies the naked triples rule to a group of cells.
        The naked triples rule identifies three cells within a group (row, column, or zone)
        that collectively contain exactly three unique notes numbers. These three numbers
        can then be eliminated from the notes of other cells in the same group.
        Args:
            group (list[list[Cell]]): A list of lists of Cell objects representing a group
                                      of cells in the sudoku grid (e.g., a row, column, or zone).
        Raises:
            ValueError: If removing a note from a cell results in an empty set of notes.
        """
        for g in group:
            # only empty cells (just in case)
            cells = [cell for cell in g if cell.val == -1]

            triples = self.find_naked_triples(cells)
            if not triples:
                continue  # no naked triples found in this g

            for cell1, cell2, cell3 in triples:
                # Restrict candidate elimination to cells in a shared zone, row, or column
                related_cells = set(g)
                if cell1.row_idx == cell2.row_idx == cell3.row_idx:
                    related_cells |= cell1.observer.row
                if cell1.col_idx == cell2.col_idx == cell3.col_idx:
                    related_cells |= cell1.observer.col
                if cell1.zone_idx == cell2.zone_idx == cell3.zone_idx:
                    related_cells |= cell1.observer.zone

                related_cells: list[Cell] = [
                    cell
                    for cell in related_cells
                    if cell not in (cell1, cell2, cell3) and cell.val == -1
                ]

                # Remove the triple's notes from the related cells
                for cell in related_cells:
                    for note in cell1.notes:
                        if note in cell.notes:
                            cell.notes.remove(note)
                            self.has_changed = True

                            # Check if removing note caused an empty set
                            if not cell.notes:
                                raise ValueError(
                                    f"Error: Cell at ({cell.row_idx}, {cell.col_idx}) ended up with an empty note set."
                                )
