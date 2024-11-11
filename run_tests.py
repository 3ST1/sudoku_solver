# ./run_tests.py
import os
import unittest

from src.SudokuSolver import SudokuSolver
from src.utils import convert_url_to_grid, delete_file


def run_test(rules: list[str], grid_file: str = None, verbose=False):
    """
    Helper function to run the test with the given rules and grid file.
    Args:
        rules (list): List of rules to apply to the grid.
        grid_file (str): Path to the grid file.
        verbose (bool): If True, the solver will print the grid at each step.

    """

    if not grid_file:
        grid_file = os.path.join(os.path.dirname(__file__), "grids/input.txt")

    if not os.path.exists(grid_file):
        raise FileNotFoundError(f"Test Failed: The file {grid_file} does not exist.")

    solver = SudokuSolver(
        input_file=grid_file, rules=rules, verbose=verbose, prompt_user=False
    )
    rules_names = [rule.name for rule in solver.rules]

    is_solved = solver.solve()
    solver.sudoku_grid.print_grid()

    if is_solved:
        print(f"Test Passed: {' & '.join(rules_names)} solved the grid successfully.")
    else:
        raise ValueError(
            f"Test Failed: {' & '.join(rules_names)} could not solve the grid."
        )


class SudokuTestRunner(unittest.TestCase):
    """
    Class that inherits from unittest.TestCase to run the tests for the SudokuSolver.
    """

    @classmethod
    def setUpClass(cls):
        """
        Method to set up the class attributes.
        """
        cls.nb_passed_tests = 0
        cls.nb_tests = len(
            [method for method in dir(cls) if method.startswith("test_")]
        )

    def run_test_case(
        self,
        rules: list,
        grid_file: str,
        test_name: str,
        verbose=False,
        test_must_fail=False,
    ) -> None:
        """
        Method to run a test case.
        Args:
            rules (list): List of rules to apply to the grid.
            grid_file (str): Path to the grid file.
            test_name (str): Name of the test.
            verbose (bool): If True, the solver will print the grid at each step.
            test_must_fail (bool): If True, the test must fail (it is maybe not the best way to test if the test fails...).

        """
        print("\n" + "=" * 25 + f" Running test {test_name} ".upper() + "=" * 25)
        try:
            tempfile = False
            if grid_file.startswith("http"):  # Check if the grid is from a URL
                grid_file = convert_url_to_grid(grid_file)
                tempfile = True

            run_test(rules, grid_file, verbose=verbose)

            if tempfile:
                delete_file(grid_file)

            if not test_must_fail:
                SudokuTestRunner.nb_passed_tests += 1
        except Exception as e:
            if test_must_fail:
                print(f"Test Passed: {test_name} failed as expected: {e}")
                SudokuTestRunner.nb_passed_tests += 1
            else:
                self.fail(f"{test_name} failed: {e}")
        finally:
            print(
                f"{SudokuTestRunner.nb_passed_tests}/{self.__class__.nb_tests} tests passed."
            )

    ########## NAKED STRATEGIES TESTS ##########
    def test_naked_singles(self):
        self.run_test_case(
            ["naked_singles"],
            "https://www.sudokuwiki.org/sudoku.htm?bd=246975138589316274371040695498621753132754986657830421724183569865492317913567842",
            "test_naked_singles",
        )

    def test_naked_pairs(self):
        self.run_test_case(
            ["naked_singles", "naked_pairs"],
            "https://www.sudokuwiki.org/sudoku.htm?bd=080090030030000000002060108020800500800907006004005070503040900000000010010050020",
            "test_naked_pairs",
        )

    def test_naked_triples(self):
        self.run_test_case(
            ["naked_singles", "naked_pairs", "naked_triples"],
            "https://www.sudokuwiki.org/sudoku.htm?bd=070008029002000004854020000008374200000000000003261700000090612200000400130600070",
            "test_naked_triples",
        )

    ########## HIDDEN STRATEGIES TESTS ##########
    def test_hidden_singles(self):
        self.run_test_case(
            ["hidden_singles"],
            "https://www.sudokuwiki.org/sudoku.htm?bd=200070038000006070300040600008020700100000006007030400004080009060400000910060002",
            "test_hidden_singles",
        )

    def test_hidden_pairs(self):
        self.run_test_case(
            ["hidden_singles", "hidden_pairs"],
            "https://www.sudokuwiki.org/sudoku.htm?bd=000000000904607000076804100309701080008000300050308702007502610000403208000000000",
            "test_hidden_pairs",
        )

    def test_hidden_triples(self):
        self.run_test_case(
            [
                "hidden_singles",
                "hidden_pairs",
                "hidden_triples",
                "naked_pairs",
                "naked_triples",
            ],
            "https://www.sudokuwiki.org/sudoku.htm?bd=000000000231090000065003100008924000100050006000136700009300570000010843000000000",
            "test_hidden_triples",
        )

    ########## THOUGH STRATEGIES TEST ##########
    def test_y_wing(self):
        self.run_test_case(
            [
                "hidden_singles",
                "hidden_pairs",
                "naked_pairs",
                "naked_triples",
                "y_wing",
            ],
            "https://www.sudokuwiki.org/sudoku.htm?bd=720400030000000047001076802010039000000801000000260080209680400340000000060003075",
            "test_y_wing",
        )

    ########## FAILURE TESTS ##########
    def test_incomplete_grid(self):
        self.run_test_case(
            [],  # all rules
            "grids/incomplete.txt",
            "test_incomplete_grid",
            test_must_fail=True,  # this may not be the optimal way to test if test fails
        )

    def test_impossible_grid(self):
        self.run_test_case(
            [],  # all rules
            "grids/impossible.txt",
            "test_impossible_grid",
            test_must_fail=True,
        )

    def test_false_grid(self):
        self.run_test_case(
            [],  # all rules
            "grids/false.txt",
            "test_false_grid",
            test_must_fail=True,
        )

    def test_unknwon_rule(self):
        self.run_test_case(
            ["unknown_rule"],
            "grids/very_hard.txt",
            "test_unknown_rule",
            test_must_fail=True,  # must fail because the rule is unknown (not in the DeductionRuleFactory)
        )

    def test_very_hard(self):
        self.run_test_case(
            [],
            "grids/very_hard.txt",
            "test_very_hard",
            test_must_fail=True,  # must fail because we do not prompt the user for input in these test
        )


if __name__ == "__main__":
    unittest.main()
