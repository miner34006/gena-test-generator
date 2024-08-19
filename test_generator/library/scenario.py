from dataclasses import dataclass, field


@dataclass
class TestScenario:
    priority: str
    test_name: str = field(repr=False)
    subject: str
    description: str = field(repr=False)
    expected_result: str
    is_positive: bool = field(repr=False)
    params: list[str] = field(default_factory=list, repr=False)

    scenario_data: dict = field(default_factory=dict, repr=False)

    @staticmethod
    def create_empty() -> 'TestScenario':
        return TestScenario(
            priority='',
            test_name='',
            subject='',
            description='',
            expected_result='',
            is_positive=False
        )
