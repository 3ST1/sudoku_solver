from src.DeductionRules.DeductionRule import DeductionRule
from src.SudokuGrid import Cell, SudokuGrid


class DR3(DeductionRule):
    def __init__(self, d: int = None) -> None:
        self.name = "Y Wing"
        self.difficulty = d or 3

    def _apply_rule(self, grid: SudokuGrid):
        # Return the result of apply_y_wing, True if something changes, False otherwise
        self.apply_y_wing(grid)

    def get_cells_seen_by_pincers(
        self, pivot: Cell, pincer1: Cell, pincer2: Cell
    ) -> list[Cell]:
        """
        Returns all cells that are in the same row, column, or zone as both pincer1 and pincer2.
        Args:
            pivot (Cell): The pivot cell of the Y-Wing.
            pincer1 (Cell): The first pincer cell of the Y-Wing.
            pincer2 (Cell): The second pincer cell of the Y-Wing.
        Returns:
            list[Cell]: A list of Cell objects that are in the same row, column, or zone as both pincer1 and pincer2.
        """
        seen_by_pincers = set()

        # get pincer1 related cells
        cells_pincer_1 = pincer1.observer.related_cells
        cells_pincer_1 = [
            cell
            for cell in cells_pincer_1
            if cell.val == -1 and cell not in [pivot, pincer1, pincer2]
        ]

        # get pincer2 related cells
        cells_pincer_2 = pincer2.observer.related_cells
        cells_pincer_2 = [
            cell
            for cell in cells_pincer_2
            if cell.val == -1 and cell not in [pivot, pincer1, pincer2]
        ]

        # get cells seen by both pincers
        for cell in cells_pincer_1:
            if cell in cells_pincer_2:
                seen_by_pincers.add(cell)

        return seen_by_pincers

    def apply_y_wing(self, grid: SudokuGrid):
        """
        Apply the Y-Wing deduction rule.
        The Y-Wing technique involves identifying a pivot cell with exactly two notes
        and two pincer cells that share one note with the pivot and one note with each other.
        If this configuration is found, the common note between the pincers can be eliminated from
        any cell that are seen by both pincers.
        Args:
            grid (SudokuGrid): The Sudoku grid to which the Y-Wing rule will be applied.
        Returns:
            None
        """

        # Iterate through each cell in the grid
        for pivot in grid():
            # The pivot cell must be empty and have exactly two possible candidates (notes)
            if pivot.val != -1 or len(pivot.notes) != 2:
                continue

            possible_pincers = []

            # Get all the cells in the same row, column, or zone as the pivot
            cells = [
                cell
                for cell in pivot.observer.related_cells
                if cell.val == -1 and len(cell.notes) == 2 and cell != pivot
            ]

            # Identify potential pincers that share exactly one note with the pivot
            for cell in cells:
                if len(pivot.notes & cell.notes) == 1:
                    possible_pincers.append(cell)

            # Find a pair of pincers satisfying Y-Wing conditions
            for i, pincer1 in enumerate(possible_pincers):
                for pincer2 in possible_pincers[i + 1 :]:  # Avoid duplicate pairs
                    # Check three unique notes and one shared note between pincers
                    if (
                        len(pivot.notes | pincer1.notes | pincer2.notes) == 3
                        and len(pincer1.notes & pincer2.notes) == 1
                    ):
                        common_candidate = (pincer1.notes & pincer2.notes).pop()

                        # Get cells seen by both pincers for elimination
                        for cell in self.get_cells_seen_by_pincers(
                            pivot, pincer1, pincer2
                        ):
                            if common_candidate in cell.notes:
                                # print(
                                #     f"Y-Wing found: pivot ({pivot.row_idx}, {pivot.col_idx}) "
                                #     f"with pincers ({pincer1.row_idx, pincer1.col_idx}, {pincer2.row_idx, pincer2.col_idx}), "
                                #     f"target cell ({cell.row_idx}, {cell.col_idx}) with notes {cell.notes} containing {common_candidate}"
                                # )
                                cell.notes.remove(common_candidate)
                                self.has_changed = True
                                return  # we stop when we find a ywing
