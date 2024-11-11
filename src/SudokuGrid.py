# ./src/SudokuGrid.py
from copy import copy

from src.Cell import Cell, CellObserver
from src.utils import is_unique


class SudokuGrid:
    """
    A class to represent a Sudoku grid.
    The grid is represented as a list of 81 Cell objects.
    """

    def __init__(self, grid: list[int]) -> None:
        """
        Initialize a SudokuGrid from a list of 81 integers.
        Args:
            grid (list[int]): A list of 81 integers representing the Sudoku grid.
        Attributes:
            rows (list[list[Cell]]): A 9x9 list of Cell objects representing the rows of the grid.
            cols (list[list[Cell]]): A 9x9 list of Cell objects representing the columns of the grid.
            zones (list[list[Cell]]): A 9x9 list of Cell objects representing the 3x3 zones of the grid.
        """

        # Ensure the input grid is a list of 81 integers
        if len(grid) != 81:
            raise ValueError("Grid must be a list of 81 integers.")

        # Initialize rows, cols, and zones with empty lists
        self.rows: list[list[Cell]] = [[None for _ in range(9)] for _ in range(9)]
        self.cols: list[list[Cell]] = [[None for _ in range(9)] for _ in range(9)]
        self.zones: list[list[Cell]] = [[None for _ in range(9)] for _ in range(9)]

        # Populate the grid with Cell objects
        for i, val in enumerate(grid):
            # get the row index by dividing the index by 9
            row_idx = i // 9
            # get the column index by getting the rest of the division by 9
            col_idx = i % 9
            cell = Cell(row_idx, col_idx, val)

            # Assign cell to rows, columns, and zones
            self.rows[row_idx][col_idx] = cell
            self.cols[col_idx][row_idx] = cell
            zone_idx = cell.zone_idx
            # Find the next empty cell in the zone and assign the cell to it
            self.zones[zone_idx][self.zones[zone_idx].index(None)] = cell

        # Initialize the observer for each cell
        for cell in self():
            cell.observer = CellObserver(self, cell)

        self.compute_cell_notes()

    def __call__(self) -> list[Cell]:
        """
        Return the list of 81 Cell representing the current state of the grid.
        Returns:
            list[Cell]: A list of 81 Cell objects.
        """
        return [cell for row in self.rows for cell in row]

    def get_int_list(self):
        """
        Return the list of 81 int representing the current values of the grid.
        Returns:
            list[int]: A list of 81 integers representing the grid.
        """
        return [cell.val for row in self.rows for cell in row]

    def create_bckp(self):
        """
        Create a backup of the current grid.
        Returns:
            SudokuGrid: A copy of the current grid.
        """
        return copy(self)

    def compute_cell_notes(self):
        """
        Calculate and set the possible values (notes) for each empty cell.
        Returns:
            None
        """

        for row in self.rows:
            for cell in row:
                if cell.val == -1:  # Only calculate notes for empty cells
                    cell.notes = self.get_possible_values(cell)

    def get_possible_values(self, cell: Cell) -> set[int]:
        """
        Return a set of possible values (1-9) that can go into the given cell.
        Args:
            cell (Cell): The cell for which to calculate the possible values.
            Returns:
            set[int]: A set of possible values that can go into the cell.
        """
        # Collect values already in the same row, column, and zone
        used_values = set()

        # Add values from the same row
        used_values.update(c.val for c in self.rows[cell.row_idx] if c.val != -1)

        # Add values from the same column
        used_values.update(c.val for c in self.cols[cell.col_idx] if c.val != -1)

        # Add values from the same zone
        used_values.update(c.val for c in self.zones[cell.zone_idx] if c.val != -1)

        # Possible values are the numbers 1-9 that are not in the used_values
        # at start cell.notes contains all possible values (1-9)
        return cell.notes - used_values

    def get_cell(self, row_idx: int, col_idx: int) -> Cell:
        """
        Get the cell at the specified row and column.
        Args:
            row_idx (int): The row index (0-8).
            col_idx (int): The column index (0-8).
        Returns:
            Cell: The cell at the specified row and column.
        """
        if not isinstance(row_idx, int) or not isinstance(col_idx, int):
            raise TypeError("<row_idx> & <col_idx> must be int")
        if row_idx not in range(0, 9) or col_idx not in range(0, 9):
            raise ValueError(
                f"<row_idx> (={row_idx}) & <col_idx> (={col_idx}) must be in range 0-9"
            )
        return self.rows[row_idx][col_idx]

    def is_complete(self) -> bool:
        """
        Check if the grid is complete by looking for -1 in the array.
        Returns:
            bool: True if the grid is complete, False otherwise.
        """
        return all(value != -1 for value in self.get_int_list())

    def is_correct(self) -> bool:
        """
        Check if the grid is correct.
        A grid is correct if there are no duplicate values in rows, columns, or zones.
        Returns:
            bool: True if the grid is correct, False otherwise.
        """

        def _check_duplicates(group: list[list[Cell]]) -> bool:
            """
            Check if there are any duplicate values in a group of cells.
            Args:
                group (list[list[Cell]]): A list of lists of Cell objects.
            Returns:
                bool: True if there are no duplicates, False otherwise.
            """
            for g in group:
                values = [c.val for c in g]
                if not is_unique(values):
                    return False
            return True

        # Check rows for duplicates
        if not _check_duplicates(self.rows):
            return False
        # Check columns for duplicates
        if not _check_duplicates(self.cols):
            return False
        # Check 3x3 zones for duplicates
        if not _check_duplicates(self.zones):
            return False

        return True

    def print_grid(self):
        """
        Prints the Sudoku grid.
        Empty cells are shown as dots ('.').
        The grid is formatted as a 9x9 grid with divisions between 3x3 subgrids.
        Returns:
            None
        """
        # Get the grid as a list of integers
        grid = self.get_int_list()

        for row in range(9):
            for col in range(9):
                value = grid[row * 9 + col]
                print(value if value != -1 else ".", end=" ")
                if (col + 1) % 3 == 0 and col != 8:
                    print("|", end=" ")
            print()
            if (row + 1) % 3 == 0 and row != 8:
                print("-" * 21)

    def show_notes(self):
        """
        Print the notes for each cell in the grid.
        Returns:
            None
        """
        for cell in self():
            if cell.val == -1:
                print(f"{cell.row_idx+1}-{cell.col_idx+1} : {cell.notes}")
                print(f"{cell.row_idx+1}-{cell.col_idx+1} : {cell.notes}")
