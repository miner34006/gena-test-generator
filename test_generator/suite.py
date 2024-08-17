from dataclasses import dataclass, field

from .scenario import TestScenario


@dataclass
class Suite:
    feature: str
    story: str
    test_scenarios: list[TestScenario] = field(default_factory=list)

    other_data: dict = field(default_factory=dict, repr=False)

    api_endpoint: str = ''
    api_method: str = ''

    @staticmethod
    def create_empty_suite() -> "Suite":
        return Suite(feature='', story='', test_scenarios=[], api_endpoint='', api_method='')
