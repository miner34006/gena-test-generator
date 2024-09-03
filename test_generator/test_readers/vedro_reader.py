import ast
import os

from test_generator.library.colors import Colors
from test_generator.library.errors import ScenariosValidationError
from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite
from test_generator.test_readers.base_reader import BaseReader


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


class VedroReader(BaseReader):
    name = 'VedroReader'

    def read_test(self, file_path: str, *args, **kwargs) -> tuple[str, str, TestScenario | None]:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)

        visitor = ScenarioVisitor()
        visitor.visit(tree)
        if not visitor.was_found:
            return '', '', None
        return visitor.feature, visitor.story, visitor.scenario

    def read_tests(self, target_dir: str, *args, **kwargs) -> Suite:
        stories = set()
        features = set()
        scenarios = []

        all_objects_in_dir = os.listdir(target_dir)
        for object_path in all_objects_in_dir:
            if os.path.isdir(os.path.join(target_dir, object_path)):
                suite = self.read_tests(os.path.join(target_dir, object_path))
                if suite.test_scenarios:
                    stories.add(suite.suite_data['story'])
                    features.add(suite.suite_data['feature'])
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
            raise ScenariosValidationError(Colors.error(f"Multiple features detected: {features}, "
                                           "can't create a single scenarios file."))
        if (len(stories) > 2) or (len(stories) == 2 and ScenarioVisitor.unknown not in stories):
            raise ScenariosValidationError(Colors.error(f"Multiple stories detected: {stories}, "
                                           "can't create a single scenarios file."))

        feature = ' & '.join(list(features))
        story = ' & '.join(list(stories))

        return Suite(
            test_scenarios=scenarios,
            suite_data={
                'feature': feature,
                'story': story,
                'API': f"{ScenarioVisitor.unknown} {ScenarioVisitor.unknown}",
            }
        )
