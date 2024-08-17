import argparse
import os
from copy import deepcopy

from test_generator.chatgpt_handler import ChatGPTHandler
from test_generator.md_handlers import get_default_md_handler, get_md_handler_by_name, get_md_handlers
from test_generator.test_handlers.vedro_handler import VedroHandler


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
    parser.add_argument('--template-path', type=str, required=True,
                        help='Path to the template file.')
    parser.add_argument('--target-dir', type=str,
                        help='Directory to put or read generated test files. '
                             'Defaults to the directory of scenarios-path.')
    parser.add_argument('--ai', action='store_true', help='Use AI to generate test file names and subjects.')
    parser.add_argument('--md-format', type=valid_md_format,
                        help=f"Name of the format to use. "
                             f"Available scenarios.md formats are: "
                             f"{','.join([f.format_name for f in get_md_handlers()])}",
                        default=get_default_md_handler().format_name)
    parser.add_argument('--force', action='store_true', help='Force overwrite existing files.')
    return parser.parse_args()


def get_script_paths(args: argparse.Namespace) -> tuple:
    current_dir = os.getcwd()
    scenarios_path = os.path.join(current_dir, args.scenarios_path)
    target_dir = os.path.join(current_dir, args.target_dir) \
        if args.target_dir else os.path.dirname(scenarios_path)
    return scenarios_path, args.template_path, target_dir


def main(args: argparse.Namespace) -> None:
    scenarios_path, template_path, target_dir = get_script_paths(args)

    md_handler = get_md_handler_by_name(args.md_format)
    md_handler.validate_scenarios(scenarios_path)
    suite = md_handler.read_data(scenarios_path)

    if args.ai:
        key = os.environ.get('OPENAI_API_KEY', '')
        base_url = os.environ.get('OPENAI_URL', '')
        suite = ChatGPTHandler(key=key, base_url=base_url).update_suite(deepcopy(suite))

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    test_handler = VedroHandler(template_content)
    test_handler.validate_suite(suite)
    test_handler.write_tests(dir_path=target_dir, suite=suite, force=args.force)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
