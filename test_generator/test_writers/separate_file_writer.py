import os
from dataclasses import asdict

from jinja2 import Environment, FileSystemLoader, Template

from test_generator.library.colors import Colors
from test_generator.library.errors import ScenariosValidationError
from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite
from test_generator.test_writers.base_writer import BaseWriter


class SeparateFileWriter(BaseWriter):
    name = 'SeparateFileWriter'

    def __init__(self, template_path: str) -> None:
        super().__init__()
        self.template = self.__get_template(template_path)

    def __get_template(self, template_path: str) -> Template:
        if not os.path.exists(template_path):
            raise ScenariosValidationError(Colors.error(f"Template file not found: {template_path}"))

        template_dir = os.path.dirname(template_path)
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template_name = os.path.basename(template_path)
        return env.get_template(template_name)

    def write_test(self, file_path: str, scenario: TestScenario,
                   force: bool = False, other_template_data: dict = None, *args, **kwargs) -> None:
        if not force and os.path.exists(file_path):
            print(Colors.warning(f"⚠️ File already exists: {file_path}"))
            return

        content = self.template.render(
            **other_template_data if other_template_data else {},
            **asdict(scenario)
        )
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(Colors.success(f"✅  Test file created: {file_path}"))

    def write_tests(self, dir_path: str, suite: Suite, force: bool = False, *args, **kwargs) -> None:
        print(Colors.bold(f"📝 Generating tests..."))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for scenario in suite.test_scenarios:
            test_path = os.path.join(dir_path, self.get_file_name(scenario))

            other_template_data = asdict(suite)
            other_template_data.pop('test_scenarios')

            self.write_test(
                file_path=test_path,
                scenario=scenario,
                other_template_data=other_template_data,
                force=force
            )

    def validate_suite(self, suite: Suite, *args, **kwargs) -> None:
        if not suite.test_scenarios:
            raise ScenariosValidationError(Colors.error('No test scenarios defined in suite'))

    @staticmethod
    def get_file_name(scenario: TestScenario) -> str:
        file_name = scenario.test_name or f"{scenario.subject.strip().replace(' ', '_').replace('-', '_').lower()}.py"
        return file_name
