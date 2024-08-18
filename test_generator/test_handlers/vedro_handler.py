import ast
import os

from test_generator.library.errors import ScenariosValidationError
from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite
from test_generator.test_handlers.test_handler import TestHandler

PARAMS_TEMPLATE = """\n
    $params
    def __init__(self, param):
        self.param = param"""


class ScenarioVisitor(ast.NodeVisitor):
    unknown = 'unknown'

    def __init__(self) -> None:
        self.feature = self.unknown
        self.story = self.unknown

        self.was_found = False
        self.scenario = TestScenario.create_empty()
        self.scenario.priority = self.unknown
        self.scenario.description = self.unknown
        self.scenario.subject = self.unknown
        self.scenario.expected_result = self.unknown

    def __cut_subject_params(self, subject: str) -> str:
        return subject.split(' (param = ')[0]

    def visit_ClassDef(self, node):
        if any(self.is_scenario_base(base) for base in node.bases):
            self.was_found = True
            self.visit_scenario_decorators(node.decorator_list)
            self.visit_class_body(node.body)

    def is_scenario_base(self, base: ast.Name | ast.Attribute) -> bool:
        if isinstance(base, ast.Name):
            return base.id == 'Scenario'
        elif isinstance(base, ast.Attribute):
            return base.attr == 'Scenario'

    def visit_scenario_decorators(self, decorator_list: list) -> None:
        if not decorator_list:
            return

        decorator = decorator_list[0]
        for arg in decorator.args:
            if not isinstance(arg, ast.Attribute):
                continue
            id = arg.value.id  # type: ignore
            if id == 'Feature':
                self.feature = arg.attr
            elif id == 'Story':
                self.story = arg.attr
            elif id == 'Priority':
                self.scenario.priority = arg.attr

    def visit_class_body(self, body) -> None:
        for item in body:
            if isinstance(item, ast.Expr) and isinstance(item.value, ast.Str):
                self.parse_docstring(item.value.s)
            elif isinstance(item, ast.Assign) and item.targets[0].id == 'subject':  # type: ignore
                subject = self.__cut_subject_params(item.value.s)  # type: ignore
                self.scenario.subject = subject
                self.scenario.is_positive = 'try to' not in subject.lower()
            elif isinstance(item, ast.FunctionDef) and item.name == '__init__':
                self.parse_test_params(item)

    def parse_docstring(self, docstring: str) -> None:
        for line in docstring.split('\n'):
            if line.strip().startswith('Ожидаемый результат:'):
                self.scenario.expected_result = line.split(':', 1)[1].strip()
                break

        expected_result = f'Ожидаемый результат: {self.scenario.expected_result}'
        description = docstring.replace(expected_result, '').strip()
        self.scenario.description = " ".join(description.split())

    def parse_test_params(self, node) -> None:
        params = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and decorator.func.attr == 'params':  # type: ignore
                for arg in decorator.args:
                    if isinstance(arg, ast.Constant):
                        params.append(arg.value)
                    if isinstance(arg, ast.Name):
                        params.append(arg.id)
                    if isinstance(arg, ast.Attribute):
                        params.append(arg.attr)

        self.scenario.params = params


class VedroHandler(TestHandler):
    def __init__(self, template: str = None) -> None:
        super().__init__()
        self.template = template

    def read_test(self, file_path: str, *args, **kwargs) -> tuple[str, str, TestScenario | None]:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)

        visitor = ScenarioVisitor()
        visitor.visit(tree)
        if not visitor.was_found:
            return '', '', None
        return visitor.feature, visitor.story, visitor.scenario

    def write_test(self, file_path: str, scenario: TestScenario, feature: str, story: str,
                   force: bool = False, *args, **kwargs) -> None:
        if not self.template:
            raise RuntimeError('Template is not defined for writing tests')

        filled_template = self.template.replace('$feature', feature) \
                                       .replace('$story', story) \
                                       .replace('$priority', scenario.priority) \
                                       .replace('$subject', self.__get_subject(scenario)) \
                                       .replace('$description', scenario.description) \
                                       .replace('$expected_result', scenario.expected_result) \
                                       .replace('$params', self.__get_params(scenario))
        if not force and os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(filled_template)

        print(f"Test file created: {file_path}")

    def write_tests(self, dir_path: str, suite: Suite, force: bool = False, *args, **kwargs) -> None:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for scenario in suite.test_scenarios:
            test_path = os.path.join(dir_path, self.get_file_name(scenario))
            self.write_test(
                file_path=test_path,
                scenario=scenario,
                feature=suite.feature,
                story=suite.story,
                force=force
            )

    @staticmethod
    def get_file_name(scenario: TestScenario) -> str:
        file_name = scenario.test_name or f"{scenario.subject.strip().replace(' ', '_').replace('-', '_').lower()}.py"
        return file_name

    def read_tests(self, target_dir: str, *args, **kwargs) -> Suite:
        stories = set()
        features = set()
        scenarios = []

        all_objects_in_dir = os.listdir(target_dir)
        for object_path in all_objects_in_dir:
            if os.path.isdir(os.path.join(target_dir, object_path)):
                suite = self.read_tests(os.path.join(target_dir, object_path))
                if suite.test_scenarios:
                    stories.add(suite.story)
                    features.add(suite.feature)
                    scenarios.extend(suite.test_scenarios)
                    continue

            if not object_path.endswith('.py'):
                continue

            feature, story, scenario = self.read_test(os.path.join(target_dir, object_path))
            if scenario:
                scenarios.append(scenario)
            if story:
                stories.add(story)
            if feature:
                features.add(feature)

        if (len(features) > 2) or (len(features) == 2 and ScenarioVisitor.unknown not in features):
            raise ScenariosValidationError(f"Multiple features detected: {features}, "
                                           "can't create a single scenarios file.")
        if (len(stories) > 2) or (len(stories) == 2 and ScenarioVisitor.unknown not in stories):
            raise ScenariosValidationError(f"Multiple stories detected: {stories}, "
                                           "can't create a single scenarios file.")

        feature = ' & '.join(list(features))
        story = ' & '.join(list(stories))

        return Suite(
            feature=feature,
            story=story,
            test_scenarios=scenarios,
            api_endpoint=ScenarioVisitor.unknown,
            api_method=ScenarioVisitor.unknown
        )

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
