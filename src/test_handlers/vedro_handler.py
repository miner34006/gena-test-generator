from src.test_handlers.test_handler import TestHandler
from src.scenario import TestScenario
from src.suite import Suite
from src.errors import ScenariosValidationError
import os


class VedroHandler(TestHandler):
    def __init__(self, template: str) -> None:
        super().__init__()
        self.template = template

    def read_test(self, file_path: str, *args, **kwargs) -> TestScenario:
        raise NotImplementedError('method is not implemented')

    def write_test(self, file_path: str, scenario: TestScenario, feature: str, story: str, *args, **kwargs) -> None:
        scenario.update_subject()
        filled_template = self.template.replace('$feature', feature) \
                                       .replace('$story', story) \
                                       .replace('$priority', scenario.priority) \
                                       .replace('$subject', scenario.subject) \
                                       .replace('$description', scenario.description) \
                                       .replace('$expected_result', scenario.expected_result) \
                                       .replace('$params', scenario.get_params_template())

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(filled_template)

        print(f"Test file created: {file_path}")

    def write_tests(self, dir_path: str, suite: Suite, *args, **kwargs) -> None:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for scenario in suite.test_scenarios:
            test_path = os.path.join(dir_path, scenario.test_name)
            self.write_test(file_path=test_path, scenario=scenario, feature=suite.feature, story=suite.story)


    def validate_suite(self, suite: Suite, *args, **kwargs) -> None:
        if not suite.feature:
            raise ScenariosValidationError('Feature is not defined')
        if not suite.story:
            raise ScenariosValidationError('Story is not defined')
        if not suite.test_scenarios:
            raise ScenariosValidationError('No test scenarios defined')
        for scenario in suite.test_scenarios:
            if not scenario.priority:
                raise ScenariosValidationError(f'Priority is not defined for scnenario {scenario}')
            if not scenario.subject:
                raise ScenariosValidationError(f'Subject is not defined for scnenario {scenario}')
            if not scenario.test_name:
                raise ScenariosValidationError(f'Test name is not defined for scnenario {scenario}')
