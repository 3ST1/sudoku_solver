# ./main.py
import argparse

from src.SudokuSolver import SudokuSolver


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle.")
    parser.add_argument(
        "--input", type=str, default=None, help="Path to use another input file"
    )
    parser.add_argument(
        "--verbose", type=str, default="False", help="Enable verbose output"
    )
    parser.add_argument(
        "--prompt_user", type=str, default="True", help="Prompt user for input"
    )
    args = parser.parse_args()

    # Create a SudokuSolver instance with the provided args
    solver = SudokuSolver(
        args.input,
        verbose=args.verbose == "True",
        prompt_user=args.prompt_user == "True",
    )

    # Solve the sudoku
    solver.solve()

    # Print the Grid from SudokuGrid
    solver.sudoku_grid.print_grid()


if __name__ == "__main__":
    main()
