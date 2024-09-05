from dataclasses import dataclass, field

from .colors import Colors
from .scenario import TestScenario


@dataclass
class Suite:
    test_scenarios: list[TestScenario] = field(default_factory=list)

    suite_data: dict = field(default_factory=dict, repr=False)

    @staticmethod
    def create_empty_suite() -> "Suite":
        return Suite(test_scenarios=[])

    def is_applicable_for_api_or_schemas(self) -> bool:
        if 'API' not in self.suite_data:
            print(Colors.warning('➡️ API is not defined in the suite data, skipping generation...'))
            return False

        method = self.suite_data['API'].split(' ')[0]
        path = self.suite_data['API'].split(' ')[1]

        if not method or method is None or method == 'unknown':
            print(Colors.warning('➡️ API method is not defined, skipping generation...'))
            return False

        if not path or path is None or path == 'unknown':
            print(Colors.warning('➡️ API path is not defined, skipping generation'))
            return False

        return True
