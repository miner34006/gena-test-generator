import os

from test_generator.errors import ScenariosValidationError
from test_generator.priority import Priority
from test_generator.scenario import TestScenario
from test_generator.suite import Suite

from .md_handler import MdHandler

SCNEARIOS_STR = """## Описание

**Feature** - {feature}

**Story** - {story}

## Сценарии

### Позитивные
{positive_scenarios_str}
### Негативные
{negative_scenarios_str}"""


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
            elif line.startswith('### Позитивные'):
                current_section = 'positive'
            elif line.startswith('### Негативные'):
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

    def write_data(self, file_path: str, data: Suite, force: bool, *args, **kwargs) -> None:
        if not force and os.path.exists(file_path):
            raise FileExistsError(f'File "{file_path}" already exists')

        with open(file_path, 'w', encoding='utf-8') as file:
            positive_scenarios = [scenario for scenario in data.test_scenarios if scenario.is_positive]
            negative_scenarios = [scenario for scenario in data.test_scenarios if not scenario.is_positive]

            positive_scenarios_str = ''
            for scenario in positive_scenarios:
                positive_scenarios_str += f'- {scenario.priority}: {scenario.subject}: {scenario.description} ' \
                                          f'-> {scenario.expected_result}\n'
                for param in scenario.params:
                    positive_scenarios_str += '    * ' + param + '\n'

            negative_scenarios_str = ''
            for scenario in negative_scenarios:
                negative_scenarios_str += f'- {scenario.priority}: {scenario.subject}: {scenario.description} ' \
                                          f'-> {scenario.expected_result}\n'
                for param in scenario.params:
                    negative_scenarios_str += '    * ' + param + '\n'

            scenario_str = SCNEARIOS_STR.format(
                feature=data.feature,
                story=data.story,
                positive_scenarios_str=positive_scenarios_str,
                negative_scenarios_str=negative_scenarios_str
            )
            file.write(scenario_str)

    def validate_scenarios(self, file_path: str, *args, **kwargs) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        if '**Feature**' not in file_content:
            raise ScenariosValidationError('No "**Feature**" section in file')
        if '**Story**' not in file_content:
            raise ScenariosValidationError('No "**Story**" section in file')
        if '### Позитивные' not in file_content:
            raise ScenariosValidationError('No "### Позитивные" section in file')
        if '### Негативные' not in file_content:
            raise ScenariosValidationError('No "### Негативные" section in file')

        lines = file_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                self.__validate_line(line)

    def __validate_line(self, line: str) -> None:
        if line.count(':') > 2 or '->' not in line or line.count('->') > 1 or line.count(':') == 0:
            raise ScenariosValidationError(f'Failed to parse line "{line}". '
                                           'Invalid line format, line should be like:'
                                           '`- P(0/1/2): [Test name]: Description -> Expected result`')
        priority, _ = line[1:].split(':', 1)
        priority = priority.strip()
        if priority not in [p.value for p in Priority]:
            raise ScenariosValidationError(f'Failed to parse line "{line}". '
                                           f'Invalid priority "{priority}", available priorities are: '
                                           f'{[p.value for p in Priority]}')
