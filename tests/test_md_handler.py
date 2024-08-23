import unittest
import uuid
from test_generator.library.errors import ScenariosValidationError
from test_generator.md_handlers.const import DEFAULT_SUITE
from test_generator.md_handlers.md_list_handler import MdListHandler
from test_generator.library.suite import Suite

class TestMdListHandler(unittest.TestCase):
    def setUp(self):
        self.handler = MdListHandler()

    def test_read_data(self):
        file_path = "tests/test_data/md_list.md"
        data = self.handler.read_data(file_path)
        self.assertIsInstance(data, Suite)
        self.assertEqual(len(data.test_scenarios), 2)

        # validate first scenario
        self.assertEqual(data.test_scenarios[0].priority, 'P0')
        self.assertEqual(data.test_scenarios[0].subject, "YOUR SUBJECT 1")
        self.assertEqual(data.test_scenarios[0].description, "YOUR DESCRIPTION")
        self.assertEqual(data.test_scenarios[0].expected_result, "YOUR EXPECTED RESULT")
        self.assertEqual(data.test_scenarios[0].is_positive, True)
        self.assertEqual(data.test_scenarios[0].test_name, second='')
        self.assertEqual(len(data.test_scenarios[0].params), second=0)

        # validate second scenario
        self.assertEqual(data.test_scenarios[1].priority, 'P1')
        self.assertEqual(data.test_scenarios[1].subject, "YOUR TRY TO SUBJECT 2")
        self.assertEqual(data.test_scenarios[1].description, "YOUR DESCRIPTION")
        self.assertEqual(data.test_scenarios[1].expected_result, "YOUR EXPECTED RESULT")
        self.assertEqual(data.test_scenarios[1].is_positive, False)
        self.assertEqual(data.test_scenarios[1].test_name, second='')
        # validate params
        self.assertEqual(len(data.test_scenarios[1].params), second=2)
        self.assertEqual(data.test_scenarios[1].params[0], second='param_1')
        self.assertEqual(data.test_scenarios[1].params[1], second='param_2')

        # validate suite data
        self.assertEqual(data.suite_data['feature'], 'UserFeature')

    def test_read_data_without_subject(self):
        file_path = "tests/test_data/md_list_no_subject.md"
        data = self.handler.read_data(file_path)
        self.assertEqual(len(data.test_scenarios), 1)

        # validate first scenario
        self.assertEqual(data.test_scenarios[0].priority, 'P0')
        self.assertEqual(data.test_scenarios[0].subject, "")
        self.assertEqual(data.test_scenarios[0].description, "YOUR DESCRIPTION")
        self.assertEqual(data.test_scenarios[0].expected_result, "YOUR EXPECTED RESULT")
        self.assertEqual(data.test_scenarios[0].is_positive, True)
        self.assertEqual(data.test_scenarios[0].test_name, second='')

    def test_write_data(self):
        file_path = f"tests/test_data/test_generated/{uuid.uuid4()}.md"
        self.handler.write_data(file_path, DEFAULT_SUITE, force=True)

        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

            # validate headers
            self.assertIn("## Описание", file_content)
            self.assertIn("## Сценарии", file_content)
            self.assertIn("### Позитивные", file_content)
            self.assertIn("### Негативные", file_content)

            # validate suite variables
            for suite_var_name, suite_var_value in DEFAULT_SUITE.suite_data.items():
                var_str = f"**{suite_var_name}** = {suite_var_value}"
                self.assertIn(var_str, file_content)

            # validate test scenarios
            for scenario in DEFAULT_SUITE.test_scenarios:
                scenario_str = f"{scenario.priority}: {scenario.subject}: {scenario.description} -> {scenario.expected_result}"
                self.assertIn(scenario_str, file_content)
                for param in scenario.params:
                    self.assertIn(f"* {param}", file_content)

    def test_validate_scenarios_valid_md(self):
        file_path = "tests/test_data/md_list.md"
        self.handler.validate_scenarios(file_path)

    def test_validate_scenarios_invalid_md(self):
        file_path = "tests/test_data/invalid.md"
        self.assertRaises(ScenariosValidationError, self.handler.validate_scenarios, file_path)

if __name__ == "__main__":
    unittest.main()
