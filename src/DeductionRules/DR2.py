from src.DeductionRules.DeductionRule import DeductionRule
from src.SudokuGrid import Cell, SudokuGrid


class DR2(DeductionRule):
    """
    DR2 is a deduction rule base class for implementing Hidden Strategies. It inherits from the DeductionRule base class.

    """

    def __init__(self, name: str, d: int) -> None:
        self.name = name
        self.difficulty = d

    def get_notes_occurences(self, group: list[Cell]) -> dict[int, set[Cell]]:
        """
        Create a dictionary of value occurrences in the group.
        The dictionary maps a note value to a tuple containing the number of occurrences
        (of this note value in the group) and a list of cells (of the group) with that note value in their notes.
        Args:
            group (list[Cell]): A list of Cell objects representing a group (e.g., row, column, or zone) in the Sudoku Grid.

        Returns:
            dict[int, set[Cell]]: A dictionary where the keys are note values (possible candidate values for the cells)
                                  and the values are sets of Cell objects that have the corresponding note value in their notes.

        """
        notes_occurences = {}
        # Skip cells with values
        cells = [cell for cell in group if cell.val == -1]
        # Track occurrences of candidate values in this group
        for cell in cells:
            for note in cell.notes:
                if note in notes_occurences:
                    # Retrieve set of cells
                    cell_set = notes_occurences[note]
                    # add the current cell to the set of cells
                    cell_set.add(cell)
                    notes_occurences[note] = cell_set
                else:
                    # If it's the first occurrence of the note value,
                    # initialize the set of cells with the current cell
                    notes_occurences[note] = {cell}
        return notes_occurences

    def _apply_rule(self, grid: SudokuGrid):
        """
        Apply the deduction rule to the sudoku grid.
        it iterates over the rows, columns, and zones of the grid,
        and applies the deduction rule to each group (row, column, and zone).
        Args:
            grid (SudokuGrid): The Sudoku grid to which the rule will be applied.

        """
        # Apply rule to rows, cols and zones
        for unit in (grid.rows, grid.cols, grid.zones):
            for group in unit:
                # Create a dictionary of value occurrences in the group (row, col or zone)
                notes_occurences = self.get_notes_occurences(group)

                # Check for hidden singles or pairs, or triples depending on the subclass
                self.apply_hidden_rule(notes_occurences)

    def apply_hidden_rule(self, notes_occurences: dict[int, set[Cell]]):
        raise NotImplementedError("Subclasses must implement this method.")


class DR2_1(DR2):
    """
    DR2_1 is a subclass of DR2 that implements the "Hidden Singles" deduction rule.
    """

    def __init__(self, d=None):
        super().__init__(name="Hidden Singles", d=d or 1)

    def apply_hidden_rule(self, notes_occurences: dict[int, set[Cell]]):
        """
        Applies the hidden single rule to the given notes occurrences.
        The hidden single rule states that if a candidate number can only go in one cell within a unit (row, column, or zone),
        then that cell must contain that candidate number.
        If a cell is found that can only contain one note number, its value is set to that number
        Args:
            notes_occurences (dict[int, set[Cell]]): A dictionary where the keys are notes values numbers and the values are sets of cells
                                                     that can contain those notes.
        """
        for note_value, cells in notes_occurences.items():
            if len(cells) == 1:
                c: Cell = cells.pop()
                if c.val == -1:
                    c.set_value(note_value)
                    self.has_changed = True


class DR2_2(DR2):
    """
    DR2_2 class implements the hidden pairs deduction rule.
    This rule identifies pairs of numbers that are the only notes for exactly two cells in a unit (row, column, or zone).
    """

    # Implementation of the hidden pairs rule
    def __init__(self, d=None):
        super().__init__(name="Hidden Pairs", d=d or 2)

    def apply_hidden_rule(self, notes_occurences: dict[int, set[Cell]]):
        """
        Apply the hidden rule with the given notes occurrences to find and eliminate hidden pairs.
        This method checks for hidden pairs in the provided notes_occurrences dict. A hidden pair is a pair of notes that
        appear exactly in the same two cells and no other cells. When such a pair is found, all other notes in those
        cells are eliminated.
        Args:
            notes_occurences (dict[int, set[Cell]]): A dictionary where keys are note values and values are sets of
                                                     cells containing those notes.
        """
        # Check for hidden singles, pairs, and triples
        for note_1, cells_1 in notes_occurences.items():
            if not len(cells_1) == 2:
                continue

            for note_2, cells_2 in notes_occurences.items():
                if not (
                    note_2 != note_1
                    # value < v2 to avoid checking twice
                    and note_1 < note_2
                    and len(cells_2) == 2
                    # if the two sets of cells are the same, we have a hidden pair (with 2 cells) we found a hidden pair
                    and cells_1 == cells_2
                ):
                    continue

                # Now we have three sets of notes that can form a hidden triple
                cells_involved = cells_1 | cells_2

                if not len(cells_involved) == 2:
                    continue

                # print(f"Hidden pair found: {v} and {v2} in cells {cells}")
                # If we are here, we found a hidden pair
                for cell in cells_1:
                    # Eliminate all other notes except the hidden pair
                    if cell.notes - {note_1, note_2}:  # if other notes
                        cell.notes &= {note_1, note_2}  # &= : intersection update
                        self.has_changed = True


class DR2_3(DR2):
    """
    DR2_3 is a subclass of DR2 that implements the hidden triples deduction rule.

    """

    def __init__(self, d=None):
        super().__init__(name="Hidden Triples", d=d or 3)

    def apply_hidden_rule(self, notes_occurences: dict[int, set[Cell]]):
        """
        Applies the hidden triples rule with the given notes_occurrences.
        The hidden triples rule identifies three candidates that appear in exactly three cells within a unit (row, column, or zone).
        If such a triple is found, all other candidates are removed from those cells.
        Args:
            notes_occurences (dict[int, set[Cell]]): A dictionary where the keys are candidate numbers and the values are sets of cells where the candidate appears.
        """
        for note_1, cells_1 in notes_occurences.items():
            if 2 <= len(cells_1) <= 3:  # Candidate appears exactly in 2 or 3 cells
                for note_2, cells_2 in notes_occurences.items():
                    if (
                        note_2 != note_1
                        # Candidate appears exactly in 2 or 3 cells
                        and 2 <= len(cells_2) <= 3
                        # At least one cell in common
                        and 0 < len(cells_1 & cells_2) <= 3
                    ):
                        for note_3, cells_3 in notes_occurences.items():
                            if (
                                note_3 != note_1
                                and note_3 != note_2
                                # Candidate appears exactly in 2 or 3 cells
                                and 2 <= len(cells_3) <= 3
                                # At least one cell in common with both
                                and 0 < len(cells_1 & cells_3) <= 3
                                and 0 < len(cells_2 & cells_3) <= 3
                            ):
                                # Now we have three sets of notes that can form a hidden triple
                                cells_involved = cells_1 | cells_2 | cells_3

                                if not len(cells_involved) == 3:
                                    continue

                                # Update the notes for each cell involved in the hidden triple
                                for cell in cells_involved:
                                    # remove all notes that are not in the hidden triple (if hidden triple = {1, 2, 3}, and notes = {1, 2, 4, 5}, remove 4 and 5 to obtain {1, 2})
                                    if cell.notes - {note_1, note_2, note_3}:
                                        # print(
                                        #     f"Hidden Triple found for notes {note_1}, {note_2}, {note_3} in cells {[(c.row_idx, c.col_idx, c.notes) for c in cells_involved]}"
                                        # )
                                        cell.notes &= {note_1, note_2, note_3}
                                        self.has_changed = True
