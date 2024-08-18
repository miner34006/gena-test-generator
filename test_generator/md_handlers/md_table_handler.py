import os
import re
from re import Pattern

from tabulate import tabulate

from test_generator.library.errors import ScenariosValidationError
from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite

from .const import SCENARIOS_STR
from .md_handler import MdHandler


class MdTableHandler(MdHandler):
    format_name = 'md_table_format'

    def __get_header_pattern(self) -> Pattern:
        """Паттерн для заголовка таблицы"""
        return re.compile(r'\|\s*Приоритет\s*\|\s*Описание\s*\|\s*Ожидаемый\s+результат\s*\|\s*Название\s+теста\s*\|')

    def __get_separator_line_pattern(self) -> Pattern:
        """Паттерн для строки, разделяющей заголовок и строки таблицы"""
        return re.compile(r'\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|')

    def __get_rows_pattern(self) -> Pattern:
        """Паттерн для ячеек строки таблицы"""
        return re.compile(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*(?:\|\s*(.*?)\s*)?\|')

    def __get_table_pattern(self) -> Pattern:
        """Паттерн для таблицы"""
        return re.compile(r'(\|.*\|\n)(\|(?:\s*-+\s*\|)+\n)(\|.*\|\n)+')

    def __is_positive_scenario(self, current_section: str) -> bool:
        return current_section == 'positive'

    def __is_line_to_skip(self, line: str) -> bool:
        is_table_header = re.search(self.__get_header_pattern(), line) is not None
        is_table_separator = re.search(self.__get_separator_line_pattern(), line) is not None
        is_header = line.startswith('## Сценарии')
        is_title = line.startswith('## Описание')
        is_empty_line = len(re.findall(u"\\S", line)) == 0

        return is_table_header or is_table_separator or is_header or is_empty_line or is_title

    def __parse_table_line(self, line: str, current_section: str) -> TestScenario:
        rows = re.findall(self.__get_rows_pattern(), line)

        if not rows:
            raise ScenariosValidationError('Invalid rows in table')

        priority, description, expected_result, test_name = rows[0]

        subject = test_name.replace('\\', '').strip().lower() if test_name else ''

        if not description:
            raise ScenariosValidationError('Invalid table in file')

        description = description.replace('<br/>', '')
        split_description = description.split('*')
        params = [param.strip() for param in split_description[1:]]
        description = split_description[0].strip()

        return TestScenario(
            priority=priority.strip(),
            test_name='',
            subject=subject,
            description=description,
            expected_result=expected_result.strip(),
            is_positive=self.__is_positive_scenario(current_section),
            params=params
        )

    def read_data(self, file_path: str, *args, **kwargs) -> Suite:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        suite = Suite.create_empty_suite()

        current_section = None
        for line in file_content.split('\n'):
            line = line.strip()
            if line.startswith('**Feature**'):
                suite.feature = line.split('-')[1].strip()
            elif line.startswith('**API**'):
                api_with_method = line.split('-', 1)[1].strip()
                suite.api_method = api_with_method.split(' ')[0]
                suite.api_endpoint = api_with_method.split(' ')[1]
            elif line.startswith('**Story**'):
                suite.story = line.split('-')[1].strip()
            elif line.startswith('### Позитивные'):
                current_section = 'positive'
            elif line.startswith('### Негативные'):
                current_section = 'negative'
            elif self.__is_line_to_skip(line):
                continue
            elif current_section:
                suite.test_scenarios.append(self.__parse_table_line(line, current_section))

        return suite

    def __prepare_table_data_scenarios(self, scenarios: list[TestScenario], is_positive: bool) -> list[list]:
        return [
            [scenario.priority, scenario.description, scenario.expected_result, scenario.subject]
            for scenario in scenarios if scenario.is_positive == is_positive
        ]

    def write_data(self, file_path: str, data: Suite, force: bool, *args, **kwargs) -> None:
        if not force and os.path.exists(file_path):
            raise FileExistsError(f'File "{file_path}" already exists')

        headers = ["Приоритет", "Описание", "Ожидаемый результат", "Название теста"]

        positive_scenarios = self.__prepare_table_data_scenarios(data.test_scenarios, True)
        negative_scenarios = self.__prepare_table_data_scenarios(data.test_scenarios, False)

        positive_scenarios_table = tabulate(positive_scenarios, headers, tablefmt="github")
        negative_scenarios_table = tabulate(negative_scenarios, headers, tablefmt="github")

        scenarios_str = SCENARIOS_STR.format(
            feature=data.feature,
            story=data.story,
            positive_scenarios_str=positive_scenarios_table,
            negative_scenarios_str=negative_scenarios_table,
            api_method=data.api_method,
            api_endpoint=data.api_endpoint,
        )

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(scenarios_str)

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

        tables = re.findall(self.__get_table_pattern(), file_content)
        if len(tables) < 1:
            raise ScenariosValidationError('Failed to parse any table')
