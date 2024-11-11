# ./src/SudokuSolver.py
import os

from src.DeductionRuleFactory import DeductionRuleFactory
from src.DeductionRules.DeductionRule import DeductionRule
from src.RulesHandlerChain import RulesHandlerChain
from src.SudokuGrid import SudokuGrid
from src.utils import read_input, validate_input

DIFFICULTIES = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "VERY HARD"}


class SudokuSolver:
    """
    The Main Class of our Project.
    To solve a Sudoku grid using a set of deduction rules.
    """

    def __init__(
        self,
        input_file=None,
        rules: list[str] = [],
        verbose=False,
        prompt_user=True,
    ):
        """
        Initialize the SudokuSolver with the input file, rules, verbosity, and prompt_user settings.
        Args:
            input_file (str, optional): The path to the input file. Defaults to None.
            rules (list[str], optional): A list of deduction rule names to apply. Defaults to [].
            verbose (bool, optional): If True, prints additional information during solving. Defaults to False.
            prompt_user (bool, optional): If True, prompts the user for input when stuck. Defaults to True.
        Attributes:
            sudoku_grid (SudokuGrid): The Sudoku grid to solve.
            difficulty (int): The difficulty level of the grid.
            rules (list[DeductionRule]): The list of deduction rules to apply.
            rules_chain (RulesHandlerChain): The chain of rules to apply.
            verbose (bool): If True, prints additional information during solving.
            prompt_user (bool): If True, prompts the user for input when stuck.
            print_complete (function): A function to print the completion message
        """

        # if no input file is provided, use the default input file
        if not input_file:
            input_file = os.path.join(os.path.dirname(__file__), "..\grids\input.txt")

        # Read the input file and create a SudokuGrid object
        grid = read_input(input_file)
        self.sudoku_grid = SudokuGrid(grid)

        # check if the loaded grid is correct
        if not self.sudoku_grid.is_correct():
            raise ValueError(
                f"The loaded grid is not correct. please check the input file '{input_file}'"
            )

        # Initialize the difficulty level
        self.difficulty = 0

        # Create the list of deduction rules through the Factory Design Pattern
        self.rules: list[DeductionRule] = (
            [DeductionRuleFactory.create_rule(name) for name in rules]
            if rules
            else DeductionRuleFactory.create_all_rules()
        )

        # Create the chain of rules to apply -> Chain of Responsibility Design Pattern
        self.rules_chain = RulesHandlerChain(self.rules)

        # Set the verbosity and prompt_user settings
        self.verbose = verbose
        self.prompt_user = prompt_user

        # Completion message
        self.print_complete = lambda: print(
            f"Sudoku solved!\nThe level of the grid was {DIFFICULTIES.get(self.difficulty, 'UNKNOWN')}."
        )

    def apply_rules(self) -> bool:
        """
        Executes the rules chain on the sudoku grid.
        Returns:
            bool: True if the grid has changed, False otherwise.
        """
        # Execute the rules chain until a change is made or end of chain is reached
        # update the difficulty level depending on the applied rule
        has_changed, self.difficulty = self.rules_chain.execute(
            sudoku_grid=self.sudoku_grid,
            difficulty=self.difficulty,
            verbose=self.verbose,
        )
        return has_changed

    def solve(self):
        """
        Solves the Sudoku puzzle using apply_rules function.
        This function continuously applies the rules to solve the Sudoku puzzle. If the grid does not change after applying the rules,
        it either prompts the user for input (if `prompt_user` is True) or determines that the sudoku grid cannot be solved without user input.

        Returns:
            bool: True if the Sudoku puzzle is solved, False if the grid cannot be solved or is incorrect.
        """
        while True:
            # Create a backup of the grid to be able to go back if needed (not used since no backtracking at all)
            # bckp = self.sudoku_grid.create_bckp()

            # Apply the rules and check if the grid has changed
            has_changed = self.apply_rules()

            # if all the rules have been applied and the grid has not changed
            # -> we are stuck and need to ask the user for input
            if not has_changed and self.prompt_user:
                # prompt the user for input
                if self.difficulty < len(DIFFICULTIES):
                    # increase the difficulty level if not already at the maximum
                    self.difficulty += 1
                self.prompt_user_for_input(show_grid=True, show_notes=True)
            elif not has_changed and not self.prompt_user:
                # since the grid has not changed and we are not prompting the user for input
                # -> the grid cannot be solved
                if self.sudoku_grid.is_complete():
                    self.print_complete()
                    return True
                else:
                    print("The grid is stuck and cannot be solved without user input.")
                    return False

            # If the grid is incorrect -> ask the user if he wants to go back to the previous state
            # (he may have made a mistake while entering an input value) (not used since no backtracking at all)
            if not self.sudoku_grid.is_correct():
                # print("The grid is now incorrect...")
                # val = input(
                #     "Would you like to go back to the previous state ? (Yes (Y)) : "
                # )
                # if val.lower() == "y" or val.lower() == "yes":
                #     self.sudoku_grid = bckp
                #     self.sudoku_grid.print_grid()
                # else:
                # self.sudoku_grid.print_grid()

                # If the grid is still incorrect, stop the the solving process
                print("The program stopped due to an incorrect grid...")
                print("please restart the solving.")
                return False  # return False to indicate that the grid was not solved

            # if the grid is complete, print the grid and break the loop
            if self.sudoku_grid.is_complete():
                self.print_complete()
                # return True to stop the program and indicate that the grid was solved
                return True

    def prompt_user_for_input(self, show_grid=False, show_notes=False):
        """
        Prompts the user to input a row, column, and value for the Sudoku grid.
        This method will prompt the user to enter a row, column, and value, each in the range 1-9.
        It will then attempt to set the value in the Sudoku grid at the specified row and column.
        If the value cannot be set, the user will be prompted to retry.
        Args:
            show_grid (bool): If True, the current state of the Sudoku grid will be displayed before prompting for input.
            show_notes (bool): If True, the notes of remaining empty cells will be displayed to help user.
        Returns:
            None
        """

        @validate_input("row", 1, 9)
        def _get_row():
            return input("Enter row (1-9): ")

        @validate_input("column", 1, 9)
        def _get_col():
            return input("Enter column (1-9): ")

        @validate_input("value", 1, 9)
        def _get_val():
            return input("Enter value (1-9): ")

        if show_grid:
            print("\n")
            self.sudoku_grid.print_grid()
            print("The grid is not fully solved. Please provide input.")

        if show_notes:
            self.sudoku_grid.show_notes()

        row = _get_row()
        col = _get_col()
        val = _get_val()

        if not self.sudoku_grid.set_value(int(row) - 1, int(col) - 1, int(val)):
            print("Failed to set value. Please retry.")
            self.prompt_user_for_input(show_grid=show_grid, show_notes=show_notes)
