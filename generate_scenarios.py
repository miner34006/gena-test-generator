import argparse
import os
from copy import deepcopy

from test_generator.chatgpt_handler import ChatGPTHandler
from test_generator.md_handlers import get_default_md_handler, get_md_handler_by_name, get_md_handlers
from test_generator.suite import Suite
from test_generator.test_handlers.vedro_handler import VedroHandler
from test_generator.swagger_handlers.social_interface_handler import SocialInterfaceHandler


def valid_md_format(md_format: str) -> str:
    md_handlers = get_md_handlers()
    if md_format not in [f.format_name for f in md_handlers]:
        valid_formats = ','.join([f.format_name for f in md_handlers])
        raise argparse.ArgumentTypeError(f'Failed to find format, available formats are: {valid_formats}')
    return md_format


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Parse scenario file and generate scenario files from template.')
    parser.add_argument('--scenarios-path', type=str, default='scenarios.md',
                        help='Path to the scenario file. Defaults to scenarios.md in the current directory.')
    parser.add_argument('--template-path', type=str, required=False,
                        help='Path to the template file.')
    parser.add_argument('--target-dir', type=str,
                        help='Directory to put or read generated test files. '
                             'Defaults to the directory of scenarios-path.')
    parser.add_argument('--ai', action='store_true', help='Use AI to generate test file names and subjects.')
    parser.add_argument('--md-format', type=valid_md_format,
                        help="Name of the format to use. "
                             "Available scenarios.md formats are: "
                             f"{', '.join([f.format_name for f in get_md_handlers()])}",
                        default=get_default_md_handler().format_name)
    parser.add_argument('--force', action='store_true', help='Force overwrite existing files.')
    parser.add_argument('--reversed', action='store_true', help='Create scenarios file from test files.'
                                                                'Tests should have same story and feature.')
    parser.add_argument('--no-interface', action='store_true', help='Generated without interface'
                        , default=False)
    parser.add_argument('--interface-only', action='store_true', help='Generate interface only.')
    parser.add_argument('--yaml-path', type=str,
                        help='Path to the yaml file.'
                             'For generate interface or schema automatically')
    parser.add_argument('--interface-path', type=str,
                        help='Path to the interface file. '
                             'For generate interface automatically')

    return parser.parse_args()


def get_script_paths(args: argparse.Namespace) -> tuple:
    current_dir = os.getcwd()
    scenarios_path = os.path.join(current_dir, args.scenarios_path)
    target_dir = os.path.join(current_dir, args.target_dir) \
        if args.target_dir else os.path.dirname(scenarios_path)
    return scenarios_path, args.template_path, target_dir


def get_interfaces_path(args: argparse.Namespace) -> tuple:
    current_dir = os.getcwd()
    yaml_path = os.path.join(current_dir, args.yaml_path)
    interface_path = os.path.join(current_dir, args.interface_path)
    return yaml_path, interface_path


def create_tests_from_scenarios(args: argparse.Namespace) -> None:
    scenarios_path, template_path, target_dir = get_script_paths(args)

    md_handler = get_md_handler_by_name(args.md_format)
    md_handler.validate_scenarios(scenarios_path)
    suite = md_handler.read_data(scenarios_path)

    if args.interface_only:
        create_api_method_to_interface(suite, args)
        return

    if args.ai:
        key = os.environ.get('OPENAI_API_KEY', '')
        base_url = os.environ.get('OPENAI_URL', '')
        suite = ChatGPTHandler(key=key, base_url=base_url).update_suite(deepcopy(suite))

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    test_handler = VedroHandler(template_content)
    test_handler.validate_suite(suite)
    test_handler.write_tests(dir_path=target_dir, suite=suite, force=args.force)

    if not args.no_interface:
        create_api_method_to_interface(suite, args)


def create_scenarios_from_tests(args: argparse.Namespace) -> None:
    scenarios_path, _, target_dir = get_script_paths(args)

    test_handler = VedroHandler()
    suite = test_handler.read_tests(target_dir)

    md_handler = get_md_handler_by_name(args.md_format)
    md_handler.write_data(scenarios_path, suite, force=args.force)


def create_api_method_to_interface(suite: Suite, args: argparse.Namespace) -> None:

    yaml_path, interface_path = get_interfaces_path(args)

    method = suite.api_method
    path = suite.api_endpoint

    if not method or method is None:
        return
    if not path or path is None:
        return

    print(method, path)

    swagger_handler = SocialInterfaceHandler(yaml_path)
    swagger_handler.add_api_method_to_interface(interface_path, method, path)


def main(args: argparse.Namespace) -> None:
    if args.reversed:
        create_scenarios_from_tests(args)
    else:
        create_tests_from_scenarios(args)


if __name__ == '__main__':
    args = parse_arguments()

    if not args.template_path and not args.reversed:
        raise argparse.ArgumentTypeError('--template-path is required for generating tests')

    main(args)
