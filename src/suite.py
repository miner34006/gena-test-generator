from dataclasses import dataclass, field
from .scenario import TestScenario


@dataclass
class Suite:
    feature: str
    story: str
    test_scenarios: list[TestScenario] = field(default_factory=list)

    other_data: dict = field(default_factory=dict, repr=False)
