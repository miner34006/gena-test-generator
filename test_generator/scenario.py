from dataclasses import dataclass, field


@dataclass
class TestScenario:
    priority: str
    test_name: str = field(repr=False)
    subject: str
    description: str = field(repr=False)
    expected_result: str
    is_positive: bool = field(repr=False)
    params: list = field(default_factory=list, repr=False)

    other_data: dict = field(default_factory=dict, repr=False)
