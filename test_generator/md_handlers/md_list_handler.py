from enum import Enum

from test_generator.errors import ScenariosValidationError
from test_generator.scenario import TestScenario
from test_generator.suite import Suite

from .md_handler import MdHandler


class Priority(Enum):
    P0 = 'P0'
    P1 = 'P1'
    P2 = 'P2'


class MdListHandler(MdHandler):
    format_name = 'md_list_format'

    def __is_positive_scenario(self, current_section: str) -> bool:
        return current_section == 'positive'

    def __parse_line(self, line: str, current_section: str) -> TestScenario:
        priority, rest = line[1:].split(':', 1)
        priority = priority.strip()

        test_name, rest = rest.split(':', 1) if line.count(':') == 2 else ('', rest)
        description, expected_result = rest.split('->', 1)

        return TestScenario(
            priority=priority,
            test_name=f"{test_name.strip().replace(' ', '_')}.py".lower() if test_name.strip() else '',
            subject=test_name.strip(),
            description=description.strip().capitalize(),
            expected_result=expected_result.strip(),
            is_positive=self.__is_positive_scenario(current_section),
            params=[]
        )

    def read_data(self, file_path: str, *args, **kwargs) -> Suite:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        lines = file_content.split('\n')
        current_section = None
        feature = ''
        story = ''

        test_scenarios = []
        for line in lines:
            line = line.strip()
            if line.startswith('**Feature**'):
                feature = line.split('-')[1].strip()
            elif line.startswith('**Story**'):
                story = line.split('-')[1].strip()
            elif line.startswith('### позитивные'):
                current_section = 'positive'
            elif line.startswith('### негативные'):
                current_section = 'negative'
            elif line.startswith('-') and current_section:
                test_scenarios.append(self.__parse_line(line, current_section))
            elif line.startswith('*') and current_section:
                test_scenarios[-1].params.append(line.split('*')[1].strip())

        return Suite(
            feature=feature,
            story=story,
            test_scenarios=test_scenarios
        )

    def write_data(self, file_path: str, data: Suite, *args, **kwargs) -> None:
        raise NotImplementedError('method is not implemented')

    def validate_scenarios(self, file_path: str, *args, **kwargs) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        if '**Feature**' not in file_content:
            raise ScenariosValidationError('No "**Feature**" section in file')
        if '**Story**' not in file_content:
            raise ScenariosValidationError('No "**Story**" section in file')
        if '### позитивные' not in file_content:
            raise ScenariosValidationError('No "### позитивные" section in file')
        if '### негативные' not in file_content:
            raise ScenariosValidationError('No "### негативные" section in file')

        lines = file_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                self.__validate_line(line)

    def __validate_line(self, line: str) -> None:
        if line.count(':') > 2 or '->' not in line or line.count('->') > 1 or line.count(':') == 0:
            raise ScenariosValidationError(f'Failed to parse line "{line}". '
                                           f'Invalid line format, line should be like:'
                                           f'`- P(0/1/2): [Test name]: Description -> Expected result`')
        priority, _ = line[1:].split(':', 1)
        priority = priority.strip()
        if priority not in [p.value for p in Priority]:
            raise ScenariosValidationError(f'Failed to parse line "{line}". '
                                           f'Invalid priority "{priority}", available priorities are: '
                                           f'{[p.value for p in Priority]}')
