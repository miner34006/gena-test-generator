from dataclasses import dataclass, field

from .scenario import TestScenario


@dataclass
class Suite:
    test_scenarios: list[TestScenario] = field(default_factory=list)

    suite_data: dict = field(default_factory=dict, repr=False)

    @staticmethod
    def create_empty_suite() -> "Suite":
        return Suite(test_scenarios=[])
