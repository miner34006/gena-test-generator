import argparse
import os
from copy import deepcopy

from test_generator.api_handlers.api_file_updater import ApiFileUpdater
from test_generator.chatgpt_handler import ChatGPTHandler
from test_generator.helpers.path import (
    get_interface_path,
    get_scenarios_path,
    get_schemas_dir_path,
    get_target_dir_path,
    get_template_path,
    get_yaml_path,
)
from test_generator.library.colors import Colors
from test_generator.library.gena_data import get_gena_data_for_method_and_path
from test_generator.library.generate_component import GenerateComponent
from test_generator.library.suite import Suite
from test_generator.md_handlers import get_default_md_handler, get_md_handler_by_name, get_md_handlers
from test_generator.md_handlers.const import DEFAULT_SUITE
from test_generator.schema_handlers.schema_file_creator import SchemaFileCreator
from test_generator.test_readers.vedro_reader import VedroReader
from test_generator.test_writers.separate_file_writer import SeparateFileWriter


def valid_md_format(md_format: str) -> str:
    md_handlers = get_md_handlers()
    if md_format not in [f.format_name for f in md_handlers]:
        valid_formats = ','.join([f.format_name for f in md_handlers])
        raise argparse.ArgumentTypeError(Colors.error(f'❌  Failed to find format, '
                                                      f'available formats are: {valid_formats}'))
    return md_format


def valid_generate_components(generate: str) -> str:
    expected_components = list(GenerateComponent)
    generated_components = generate.split(',')
    for comp in generated_components:
        if comp not in expected_components:
            print(Colors.error(f'❌  Failed to generate - {comp.upper()}, \n'
                               f'❌  Should be contains ONLY - {", ".join(list(GenerateComponent))}.\n'
                               f'❌  Delimiter - ",".\n'))
    return generate


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Parse scenario file and generate scenario files from template.')
    parser.add_argument('--scenarios-path', type=str, default='scenarios.md',
                        help='Path to the scenario file. Defaults to scenarios.md in the current directory.')
    parser.add_argument('--template-path', type=str, required=False,
                        help='Path to the test template file (used for tests generation).')
    parser.add_argument('--api-template-path', type=str, required=False,
                        help='Path to the api template file (used for api generation).')
    parser.add_argument('--target-dir', type=str,
                        help='Directory to put or read generated test files. '
                             'Defaults to the directory of scenarios-path.')
    parser.add_argument('--md-example', action='store_true',
                        help="Generate new md-file with scenarios.", default=False)
    parser.add_argument('--ai', action='store_true', help='Use AI to generate test file names and '
                                                          'subjects for tests (if not exsists).')
    parser.add_argument('--md-format', type=valid_md_format,
                        help="Name of the format to use. "
                             "Available scenarios.md formats are: "
                             f"{', '.join([f.format_name for f in get_md_handlers()])}",
                        default=get_default_md_handler().format_name)
    parser.add_argument('--force', action='store_true', help='Force overwrite existing files.')
    parser.add_argument('--reversed', action='store_true', help='Create scenarios file from test files.'
                                                                'Tests should have same story and feature.')
    parser.add_argument('--generate', type=valid_generate_components,
                        help='\nList of generate. '
                             f'Available components are: {", ".join(list(GenerateComponent))}.\n'
                             f'Example: {",".join(list(GenerateComponent))} - generate all, '
                             f'{GenerateComponent.TESTS} - generate only tests. \n'
                             'Delimiter - ","',
                        default=GenerateComponent.TESTS)
    parser.add_argument('--yaml-path', type=str,
                        help='Path to the swagger yaml file. Used for interface generating.')
    parser.add_argument('--interface-path', type=str,
                        help='Path to the interface file. Used for interface generating.')
    parser.add_argument('--schemas-path', type=str,
                        help='Path to directory containing schemas. User for schemas generating.')

    return parser.parse_args()


def create_tests_from_scenarios(args: argparse.Namespace) -> None:
    scenarios_path = get_scenarios_path(args)

    md_handler = get_md_handler_by_name(args.md_format)
    md_handler.validate_scenarios(scenarios_path)
    suite = md_handler.read_data(scenarios_path)

    generate_components: list[str] = args.generate.split(',')

    if GenerateComponent.TESTS in generate_components:
        generate_components.remove(GenerateComponent.TESTS)
        generate_components.insert(len(generate_components), GenerateComponent.TESTS)

    for component in generate_components:

        if component == GenerateComponent.TESTS:
            print()
            suite = create_tests(suite, args)
            print()

        if component == GenerateComponent.INTERFACE:
            print()
            suite = create_api(suite, args)
            print()

        if component == GenerateComponent.SCHEMAS:
            print()
            suite = create_schemas(suite, args)
            print()


def create_scenarios_from_tests(args: argparse.Namespace) -> None:
    scenarios_path = get_scenarios_path(args)
    target_dir = get_target_dir_path(args)

    vedro_reader = VedroReader()
    suite = vedro_reader.read_tests(target_dir)
    if not suite.test_scenarios:
        print(Colors.warning(f'⚠️ No tests found in {target_dir}'))
        return

    md_handler = get_md_handler_by_name(args.md_format)
    md_handler.write_data(scenarios_path, suite, force=args.force)


def create_example_scenarios(args: argparse.Namespace) -> None:
    scenarios_path = get_scenarios_path(args)

    md_handler = get_md_handler_by_name(args.md_format)
    md_handler.write_data(scenarios_path, DEFAULT_SUITE, force=args.force)


def create_tests(suite: Suite, args: argparse.Namespace) -> Suite:
    template_path = get_template_path(args)
    target_dir = get_target_dir_path(args)

    if args.ai and not all([c.subject for c in suite.test_scenarios]):
        suite = ChatGPTHandler().update_suite(deepcopy(suite))

    test_writer = SeparateFileWriter(template_path)
    test_writer.validate_suite(suite)
    test_writer.write_tests(dir_path=target_dir, suite=suite, force=args.force)
    return suite


def create_api(suite: Suite, args: argparse.Namespace) -> Suite:
    yaml_path = get_yaml_path(args)
    interface_path = get_interface_path(args)

    if not suite.is_applicable_for_api_or_schemas():
        return suite

    method = suite.suite_data['API'].split(' ')[0]
    path = suite.suite_data['API'].split(' ')[1]

    try:
        gena_data = get_gena_data_for_method_and_path(yaml_path, method, path)
        api_generator = ApiFileUpdater(args.api_template_path)
        function_name = api_generator.add_api_method(interface_path, gena_data)
        suite.suite_data['api_function_name'] = function_name
    except Exception as e:
        print(Colors.error(f'❌  Failed to generate api interface: {e}'))
    return suite


def create_schemas(suite: Suite, args: argparse.Namespace) -> Suite:
    yaml_path = get_yaml_path(args)
    schemas_path = get_schemas_dir_path(args)

    if not suite.is_applicable_for_api_or_schemas():
        return suite

    method = suite.suite_data['API'].split(' ')[0]
    path = suite.suite_data['API'].split(' ')[1]

    try:
        gena_data = get_gena_data_for_method_and_path(yaml_path, method, path)
        schema_generator = SchemaFileCreator()
        response_schema_name = schema_generator.generate_response_schema(schemas_path, gena_data)
        suite.suite_data['response_schema_name'] = response_schema_name
    except Exception as e:
        print(Colors.error(f'❌ Failed to generate response schema: {e}\n'))
    return suite


def main() -> None:
    args = parse_arguments()

    if args.md_example:
        create_example_scenarios(args)
        return

    if args.reversed:
        create_scenarios_from_tests(args)
        return

    create_tests_from_scenarios(args)


if __name__ == '__main__':
    main()
