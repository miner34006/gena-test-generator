import argparse
import os

from src.md_handlers import get_md_handlers, get_default_md_handler
from src.test_handlers.vedro_handler import VedroHandler


def main(scenarios_path: str, template_path: str, output_dir: str, format_name: str) -> None:
    md_handlers = get_md_handlers()

    md_handler = [f for f in md_handlers if f.format_name == format_name]
    if not md_handler:
        raise ValueError(f'Failed to find format, available formats are: {[f.format_name for f in md_handlers]}')

    md_handler = md_handler[0]
    md_handler.validate_scenarios(scenarios_path)

    suite = md_handler.read_data(scenarios_path)

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    test_handler = VedroHandler(template_content)
    test_handler.validate_suite(suite)
    test_handler.write_tests(dir_path=output_dir, suite=suite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse scenario file and generate scenario files from template.')
    parser.add_argument('--file_path', type=str, default='scenarios.md',
                        help='Path to the scenario file. Defaults to scenarios.md in the current directory.')
    parser.add_argument('--template_path', type=str, required=True,
                        help='Path to the template file.')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save generated scenario files. Defaults to the directory of file_path.')

    parser.add_argument('--md-format', type=str, help=f"Name of the format to use. "\
                                                      f"Available scenarios.md formats are: {','.join([f.format_name for f in get_md_handlers()])}",
                        default=get_default_md_handler().format_name)
    args = parser.parse_args()

    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, args.file_path)
    output_dir = os.path.join(current_dir, args.output_dir) if args.output_dir else os.path.dirname(file_path)

    main(file_path, args.template_path, output_dir, args.md_format)