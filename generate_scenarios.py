import argparse
import os


def parse_scenario(line: str) -> dict:
    priority, rest = line[1:].split(':', 1)
    test_name, rest = rest.split(':', 1)
    description, expected_result = rest.split('->', 1)
    scenario = {
        'priority': priority.strip(),
        'test_name': f"{test_name.strip().replace(' ', '_')}.py",
        'subject': test_name.strip(),
        'description': description.strip().capitalize(),
        'expected_result': expected_result.strip(),
        'params': []
    }
    return scenario

def get_params_template(params: list, tab_size: int = 4) -> str:
    if not params:
        return ''

    params_template = """
    $params
    def __init__(self, param):
        self.param = param
    """
    params_str = ''
    for i, param in enumerate(params):
        params_str += f'@vedro.params("{param}")'
        if i != len(params) - 1:
            params_str += '\n' + ' ' * tab_size
    return params_template.replace('$params', params_str)


def parse_scenarios(file_content: str) -> dict:
    lines = file_content.split('\n')
    scenarios = {'positive': [], 'negative': []}
    current_section = None
    feature = ''
    story = ''

    params_added = False
    for line in lines:
        line = line.strip()
        if line.startswith('**Feature**'):
            feature = line.split('**Feature** - ')[1].strip()
        elif line.startswith('**Story**'):
            story = line.split('**Story** - ')[1].strip()
        elif line.startswith('### позитивные'):
            current_section = 'positive'
        elif line.startswith('### негативные'):
            current_section = 'negative'
        elif line.startswith('-'):
            if current_section:
                params_added = False
                scenarios[current_section].append(parse_scenario(line))
        elif line.startswith('*'):
            if current_section:
                scenarios[current_section][-1]['params'].append(line.split('*')[1].strip())
                if not params_added:
                    scenarios[current_section][-1]['subject'] += f" (param = {{param}})"
                    params_added = True

    return scenarios, feature, story

def create_scenario_files(template_content, scenarios, feature, story, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for section in ['positive', 'negative']:
        for scenario in scenarios[section]:
            filled_template = template_content.replace('$feature', feature) \
                                              .replace('$story', story) \
                                              .replace('$priority', scenario['priority']) \
                                              .replace('$subject', scenario['subject']) \
                                              .replace('$description', scenario['description']) \
                                              .replace('$expected_result', scenario['expected_result']) \
                                              .replace('$params', get_params_template(scenario['params']))

            filepath = os.path.join(output_dir, scenario['test_name'])

            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(filled_template)
            print(f"Scenario file created: {filepath}")


def main(scenarios_path: str, template_path: str, output_dir: str) -> None:
    with open(scenarios_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    parsed_scenarios, feature, story = parse_scenarios(file_content)

    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    create_scenario_files(template_content, parsed_scenarios, feature, story, output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse scenario file and generate scenario files from template.')
    parser.add_argument('--file_path', type=str, default='scenarios.md',
                        help='Path to the scenario file. Defaults to scenarios.md in the current directory.')
    parser.add_argument('--template_path', type=str, required=True,
                        help='Path to the template file.')
    parser.add_argument('--output_dir', type=str,
                        help='Directory to save generated scenario files. Defaults to the directory of file_path.')
    args = parser.parse_args()

    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, args.file_path)
    output_dir = os.path.join(current_dir, args.output_dir) if args.output_dir else os.path.dirname(file_path)

    main(file_path, args.template_path, output_dir)