from dataclasses import dataclass, field

PARAMS_TEMPLATE = """
    $params
    def __init__(self, param):
        self.param = param
"""


@dataclass
class TestScenario:
    priority: str
    test_name: str = field(repr=False)
    subject: str
    description: str = field(repr=False)
    expected_result: str
    is_positive: bool = field(repr=False)
    params: list[str] = field(default_factory=list, repr=False)

    other_data: dict = field(default_factory=dict, repr=False)


    def update_subject(self) -> None:
        append_str = f" (param = {{param}})"
        if self.params and append_str not in self.subject:
            self.subject += f" (param = {{param}})"

    def get_params_template(self, tab_size: int = 4) -> str:
        if not self.params:
            return ''

        params_str = ''
        for i, param in enumerate(self.params):
            params_str += f'@vedro.params("{param}")'
            if i != len(self.params) - 1:
                params_str += '\n' + ' ' * tab_size
        return PARAMS_TEMPLATE.replace('$params', params_str)
