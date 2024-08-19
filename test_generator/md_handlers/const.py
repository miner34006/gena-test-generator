from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite

DEFAULT_SUITE = Suite(
    suite_data={
        'feature': 'UserFeature',
        'story': 'UserStory',
        'API': 'GET /path/to/endpoint',
        'another_variable': 'another_value',
    },
    test_scenarios=[
        TestScenario(
            priority='P0',
            subject='YOUR SUBJECT 1',
            test_name='',
            description='YOUR DESCRIPTION',
            expected_result='YOUR EXPECTED RESULT',
            is_positive=True,
            params=[],
        ),
        TestScenario(
            priority='P1',
            subject='YOUR TRY TO SUBJECT 2',
            test_name='',
            description='YOUR DESCRIPTION',
            expected_result='YOUR EXPECTED RESULT',
            is_positive=False,
            params=['param_1', 'param_2', 'param_3', 'param_4'],
        ),
    ]
)
