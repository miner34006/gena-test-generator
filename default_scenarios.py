from test_generator.priority import Priority
from test_generator.scenario import TestScenario
from test_generator.suite import Suite

DEFAULT_SUITE = Suite(
    feature='UserFeature',
    story='UserStory',
    api_method='GET',
    api_endpoint='/path/to/endpoint',
    test_scenarios=[
        TestScenario(
            priority=Priority.P0.value,
            subject='do not decrease progress for in_progress achieve',
            test_name='',
            description='Вернуть меньшее число друзей чем есть сейчас для in_progress ачивки',
            expected_result='прогресс не уменьшается',
            is_positive=True,
            params=[],
        ),
        TestScenario(
            priority=Priority.P0.value,
            subject='do not decrease progress for completed achieve',
            test_name='',
            description='Вернуть меньшее число друзей чем есть сейчас для completed ачивки',
            expected_result='прогресс не уменьшается',
            is_positive=True,
            params=[],
        ),
        TestScenario(
            priority=Priority.P2.value,
            subject='try to get bonuses with invalid data',
            test_name='',
            description='Получение бонуса с невалидным параметром data',
            expected_result='Ошибка 400',
            is_positive=False,
            params=['string', 'array', 'max_int', 'negative int'],
        ),
    ]
)
