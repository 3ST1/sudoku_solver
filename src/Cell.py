# ./src/Cell.py


class CellObserver:
    """
    Observer Design Pattern
    A class to observe and update the related cells of a Cell in the Sudoku grid.
    """

    def __init__(self, grid, cell) -> None:
        """
        Initializes a CellObserver.
        Args:
            grid (SudokuGrid): The grid to which the cell belongs.
            cell (Cell): The cell being initialized.
        Attributes:
            cell (Cell): The cell being initialized.
            grid (SudokuGrid): The grid to which the cell belongs.
            row (set): A set of cells in the same row as the cell (including the cell itself).
            col (set): A set of cells in the same column as the cell (including the cell itself).
            zone (set): A set of cells in the same zone as the cell (including the cell itself).
            related_cells (set): A set of cells in the same row, column, and zone as the cell (excluding the cell itself).
        """
        self.cell = cell
        self.grid = grid

        # list of cells in cell's row (cell included)
        self.row = set(grid.rows[cell.row_idx])

        # list of cells in cell's column (cell included)
        self.col = set(grid.cols[cell.col_idx])

        # list of cells in cell's zone (cell included)
        self.zone = set(grid.zones[cell.zone_idx])

        # set of cells in the same row, column, and zone as cell (cell excluded)
        self.related_cells = self.row | self.col | self.zone
        self.related_cells.discard(cell)

    def update_cells(self):
        """
        Update the notes for cells in the same row, column, and zone after setting a value.
        Returns:
            None
        """

        for c in self.related_cells:
            if not isinstance(c, Cell):
                raise TypeError("c should be a Cell...")

            if c.val == -1:  # Only update notes for empty cells
                c.notes = self.grid.get_possible_values(c)

    def observed_cells(self) -> set:
        """
        Returns the cells that are related to this cell.
        These related cells are typically the ones in the same row, column, or zone.

        Returns:
            Set[Cell]: A set of related cells.
        """
        return self.related_cells


class Cell:
    """
    A class to represent a cell in a Sudoku grid.
    """

    def __init__(
        self, row_idx, col_idx, val: int, note: set = set(range(1, 10))
    ) -> None:
        """
        Initializes a cell in the Sudoku grid.
        Args:
            row_idx (int): The row index of the cell.
            col_idx (int): The column index of the cell.
            val (int): The value of the cell. Use 0 for empty cells.
            note (set): A set of possible notes for the cell. Default is {1, 2, 3, 4, 5, 6, 7, 8, 9}.
        Attributes:
            val (int): The value of the cell. Use -1 for empty cells.
            notes (set): A set of possible notes for the cell.
            row_idx (int): The row index of the cell.
            col_idx (int): The column index of the cell.
            zone_idx (int): The zone index of the cell.
            observer (CellObserver): The observer for the cell
        """

        self.val = val if val != 0 else -1  # Use -1 for empty cells
        self.notes = note  # Set of possible notes (if the cell is empty)

        # Indexes in the grid
        self.row_idx = row_idx  # row position
        self.col_idx = col_idx  # column position
        self.zone_idx = (self.row_idx // 3) * 3 + (self.col_idx // 3)  # 3x3 zone index

        # List of cells of the same row, column, and zone that should be notified of changes made on this cell
        self.observer: CellObserver = None

    def set_value(self, val: int) -> bool:
        """
        Set a value in the cell and notify observers if the cell was empty.
        Args:
            val (int): The value to set in the cell.
        Returns:
            bool: True if the value was set successfully, False otherwise.
        """
        if self.val == -1:  # Only allow setting if the cell was empty
            self.val = val
            if self.notes:  # Clear the remaining notes if any
                self.notes.clear()
            self.observer.update_cells()  # Update notes for related cells
            return True
        else:
            print("This cell is not empty. It won't be changed.")
            return False
