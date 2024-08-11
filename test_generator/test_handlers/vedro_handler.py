import os

from test_generator.errors import ScenariosValidationError
from test_generator.scenario import TestScenario
from test_generator.suite import Suite
from test_generator.test_handlers.test_handler import TestHandler

PARAMS_TEMPLATE = """\n
    $params
    def __init__(self, param):
        self.param = param"""


class VedroHandler(TestHandler):
    def __init__(self, template: str) -> None:
        super().__init__()
        self.template = template

    def read_test(self, file_path: str, *args, **kwargs) -> TestScenario:
        raise NotImplementedError('method is not implemented')

    def write_test(self, file_path: str, scenario: TestScenario, feature: str, story: str, *args, **kwargs) -> None:
        filled_template = self.template.replace('$feature', feature) \
                                       .replace('$story', story) \
                                       .replace('$priority', scenario.priority) \
                                       .replace('$subject', self.__get_subject(scenario)) \
                                       .replace('$description', scenario.description) \
                                       .replace('$expected_result', scenario.expected_result) \
                                       .replace('$params', self.__get_params(scenario))

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

    def __get_subject(self, scneario: TestScenario) -> str:
        append_str = " (param = {{param}})"

        subject = scneario.subject
        if scneario.params and append_str not in scneario.subject:
            subject = f"{scneario.subject} (param = {{param}})"
        return subject

    def __get_params(self, scneario: TestScenario, tab_size: int = 4) -> str:
        if not scneario.params:
            return ''

        params_str = ''
        for i, param in enumerate(scneario.params):
            params_str += f'@vedro.params("{param}")'
            if i != len(scneario.params) - 1:
                params_str += '\n' + ' ' * tab_size
        return PARAMS_TEMPLATE.replace('$params', params_str)
