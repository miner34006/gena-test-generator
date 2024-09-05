import os
from dataclasses import asdict

from jinja2 import Environment, FileSystemLoader

from test_generator.library.colors import Colors
from test_generator.library.errors import ScenariosValidationError
from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite

from .md_handler import MdHandler

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
environment = Environment(loader=FileSystemLoader(templates_dir),
                          trim_blocks=True, lstrip_blocks=True)


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
            test_name='',
            subject=test_name.strip(),
            description=description.strip(),
            expected_result=expected_result.strip(),
            is_positive=self.__is_positive_scenario(current_section),
            params=[]
        )

    def read_data(self, file_path: str, *args, **kwargs) -> Suite:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        suite = Suite.create_empty_suite()
        variables = self._find_variables(file_content)
        suite.suite_data = variables

        current_section = None
        for line in file_content.split('\n'):
            line = line.strip()
            if line.startswith('### Позитивные'):
                current_section = 'positive'
            elif line.startswith('### Негативные'):
                current_section = 'negative'
            elif line.startswith('-') and current_section:
                suite.test_scenarios.append(self.__parse_line(line, current_section))
            elif line.startswith('*') and current_section:
                suite.test_scenarios[-1].params.append(line.split('*')[1].strip())

        return suite

    def write_data(self, file_path: str, data: Suite, force: bool, *args, **kwargs) -> None:
        if not force and os.path.exists(file_path):
            raise FileExistsError(f'File "{file_path}" already exists')

        content = environment.get_template(f"{self.format_name}.jinja").render(
            **asdict(data),
        )
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def validate_scenarios(self, file_path: str, *args, **kwargs) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        if '### Позитивные' not in file_content:
            raise ScenariosValidationError(Colors.error('No "### Позитивные" section in file'))
        if '### Негативные' not in file_content:
            raise ScenariosValidationError(Colors.error('No "### Негативные" section in file'))

        lines_with_scenarios_found = False
        lines = file_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                lines_with_scenarios_found = True
                self.__validate_line(line)

        if not lines_with_scenarios_found:
            raise ScenariosValidationError(Colors.error('No scenarios with expected format were found in file'))

    def __validate_line(self, line: str) -> None:
        if line.count(':') > 2 or '->' not in line or line.count('->') > 1 or line.count(':') == 0:
            raise ScenariosValidationError(Colors.error(f'Failed to parse line "{line}". '
                                                        'Invalid line format, line should be like:'
                                                        '`- priority: [subject]: description -> expected result`'))
