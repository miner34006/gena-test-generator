import re
from re import Pattern

from test_generator.errors import ScenariosValidationError
from test_generator.scenario import TestScenario
from test_generator.suite import Suite

from .md_handler import MdHandler


class MdTableHandler(MdHandler):
    format_name = 'md_table_format'

    def __get_header_pattern(self) -> Pattern:
        """Паттерн для заголовка таблицы"""
        return re.compile(r'\|\s*Приоритет\s*\|\s*Шаги\s*\|\s*Ожидаемый\s+результат\s*\|\s*Название\s+теста\s*\|')

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

        priority, steps, expected_result, test_name = rows[0]

        if test_name:
            test_name = test_name.replace('\\', '').strip()
        else:
            test_name = "Отсутствует"  # TODO generate ai name

        if not steps:
            raise ScenariosValidationError('Invalid table in file')

        steps = steps.replace('<br/>', '')
        split_steps = steps.split('*')
        params = [param.strip() for param in split_steps[1:]]
        steps = split_steps[0]

        return TestScenario(
            priority=priority.strip(),
            test_name=f"{test_name.replace(' ', '_')}.py",
            subject=test_name,
            description=steps.strip(),
            expected_result=expected_result.strip(),
            is_positive=self.__is_positive_scenario(current_section),
            params=params
        )

    def read_data(self, file_path: str, *args, **kwargs) -> Suite:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        lines = file_content.split('\n')
        current_section = 'None'
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
            elif self.__is_line_to_skip(line):
                continue
            else:
                test_scenarios.append(self.__parse_table_line(line, current_section))

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
        if '### Позитивные' not in file_content:
            raise ScenariosValidationError('No "### Позитивные" section in file')
        if '### Негативные' not in file_content:
            raise ScenariosValidationError('No "### Негативные" section in file')

        tables = re.findall(self.__get_table_pattern(), file_content)
        if len(tables) < 1:
            raise ScenariosValidationError('Failed to parse any table')
