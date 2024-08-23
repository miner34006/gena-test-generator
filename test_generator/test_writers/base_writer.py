from abc import ABC, abstractmethod

from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite


class BaseWriter(ABC):
    name = 'AbstractBaseWriter'

    @abstractmethod
    def write_test(self, file_path: str, scenario: TestScenario, *args, **kwargs) -> None:
        """
        Записываем сценарий в файл с тестом
        """
        ...

    @abstractmethod
    def write_tests(self, dir_path: str, suite: Suite, *args, **kwargs) -> None:
        """
        Записываем сценарии в файлы
        """
        ...

    def validate_suite(self, suite: Suite, *args, **kwargs) -> None:
        """
        Проверяем сценарии на валидность
        """
        ...
