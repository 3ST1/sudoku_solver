# ./src/DeductionRuleFactory.py

from src.DeductionRules.DeductionRule import DeductionRule
from src.DeductionRules.DR1 import DR1_1, DR1_2, DR1_3
from src.DeductionRules.DR2 import DR2_1, DR2_2, DR2_3
from src.DeductionRules.DR3 import DR3


class DeductionRuleFactory:
    """
    Factory class to create DeductionRule objects.
    This class should not be instantiated directly but should be used to create DeductionRule objects.
    It provides a method to create a DeductionRule object based on the rule name and difficulty level provided.
    It also provides a method to create a list of all Deduction Rule objects.

    Attributes:
    RULES: dict: A dictionary mapping rule names to DeductionRule classes.

    Methods:
    create_rule(rule_name: str, difficulty: int): Creates a DeductionRule object based on the rule name (with the difficulty level provided).
    create_all_rules(): Creates a list of all DeductionRule objects.
    """

    RULES = {
        "naked_singles": {"class": DR1_1, "difficulty": 1},
        "naked_pairs": {"class": DR1_2, "difficulty": 2},
        "naked_triples": {"class": DR1_3, "difficulty": 2},
        "hidden_singles": {"class": DR2_1, "difficulty": 1},
        "hidden_pairs": {"class": DR2_2, "difficulty": 2},
        "hidden_triples": {"class": DR2_3, "difficulty": 3},
        "y_wing": {"class": DR3, "difficulty": 3},
    }

    @staticmethod
    def create_rule(rule_name) -> DeductionRule:
        """
        Creates and returns an instance of a deduction rule based on the provided rule name.
        Args:
            rule_name (str): The name of the rule to create.
        Returns:
            DeductionRule: An instance of the deduction rule corresponding to the provided rule name.
        Raises:
            ValueError: If the rule name is unknown or if the rule has no class defined in the RULES dictionary.
        """
        rule = DeductionRuleFactory.RULES.get(rule_name)

        if rule:
            rule_class = rule.get("class")
            if not rule_class:
                raise ValueError(
                    f"Rule {rule_name} has no class defined in the RULES dictionary in DeductionRuleFactory : {DeductionRuleFactory.RULES}"
                )
            return rule_class(rule.get("difficulty"))
        raise ValueError(f"Unknown rule: {rule_name}")

    @staticmethod
    def create_all_rules() -> list[DeductionRule]:
        """
        Creates and returns a list of all deduction rules.

        This method iterates over the RULES dictionary in the DeductionRuleFactory class,
        instantiates each rule's class with its associated difficulty, and returns a list
        of these instantiated rules.

        Returns:
            list[DeductionRule]: A list of instantiated deduction rules.
        """
        return [
            rule.get("class")(rule.get("difficulty"))
            for rule in DeductionRuleFactory.RULES.values()
            if rule.get("class")
        ]
