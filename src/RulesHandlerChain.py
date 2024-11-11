# ./src/RulesHandlerChain.py
from src.DeductionRules.DeductionRule import DeductionRule


class RuleHandler:
    """
    RuleHandler is a part of the Chain of Responsibility pattern for handling Deduction Rules.
    """

    def __init__(self, rule: DeductionRule, next_handler=None):
        """
        Initializes a RuleHandler with a given deduction rule and an optional next handler.
        Args:
            rule (DeductionRule): The deduction rule to be applied by this handler.
            next_handler (RuleHandler, optional): The next handler in the chain. Defaults to None.
        """

        self.rule: DeductionRule = rule
        self.next_handler: RuleHandler = next_handler

    def handle(self, sudoku_grid, difficulty: int, verbose: bool):
        """
        Handles the application of the DeductionRule rule. If this handler can't make changes,
        it passes handling to the next handler in the chain.
        Args:
            sudoku_grid: The Sudoku grid to which the rule will be applied.
            difficulty (int): The current difficulty level.
            verbose (bool): If True, prints additional information during rule application.
        Returns:
            tuple: A tuple containing a boolean indicating if changes were made and the updated difficulty level.
        """
        d = self.rule.get_difficulty()
        if d > difficulty:
            if verbose and difficulty > 0:
                print(f"Cannot go further with rules <= DR{difficulty}...")
                sudoku_grid.print_grid()
            difficulty = d

        # Apply the rule and check if it changes the grid
        has_changed = self.rule.apply_rule(grid=sudoku_grid, verbose=verbose)

        # If the rule has made changes -> we return True and the updated difficulty level
        if has_changed:
            return has_changed, difficulty
        # If nothing has changed -> Pass control to the next handler, if available
        elif self.next_handler:
            return self.next_handler.handle(sudoku_grid, difficulty, verbose)
        # End of chain and no changes made
        else:
            return False, difficulty


class RulesHandlerChain:
    """
    This is the Chain of Responsibility Design Pattern for handling Deduction Rules.
    RulesHandlerChain is a class that manages a chain of rule handlers for our SudokuSolver.
    Each rule handler is responsible for applying a specific deduction rule to the Sudoku grid.
    """

    def __init__(self, rules: list[DeductionRule]):
        """
        Initializes the chain of rule handlers from a list of DeductionRule instances.
        Args:
            rules (list[DeductionRule]): A list of DeductionRule instances to be added to the chain.
        """
        self.first_handler: RuleHandler = None
        self.last_handler: RuleHandler = None

        # Build the chain by adding each rule as a RuleHandler
        for rule in rules:
            self.add_handler(RuleHandler(rule))

    def add_handler(self, handler: RuleHandler):
        """
        Adds a RuleHandler to the end of the chain.
        Args:
            handler (RuleHandler): The RuleHandler to be added to the chain.
        """
        if not self.first_handler:
            self.first_handler = handler
        else:
            self.last_handler.next_handler = handler
        self.last_handler = handler

    def execute(self, sudoku_grid, difficulty: int, verbose: bool) -> tuple[bool, int]:
        """
        Starts the chain execution. Returns a tuple of whether a change was made and the updated difficulty level.
        Args:
            sudoku_grid: The Sudoku grid to which the rules will be applied.
            difficulty (int): The current difficulty level.
            verbose (bool): If True, prints additional information during rule application.
        """
        if self.first_handler:
            return self.first_handler.handle(sudoku_grid, difficulty, verbose)
        return False, difficulty  # If no handlers are in the chain
