from abc import ABC, abstractmethod
from src.scenario import TestScenario
from src.suite import Suite


class TestHandler(ABC):
    name = 'AbstractTestHandler'

    @abstractmethod
    def read_test(self, file_path: str, *args, **kwargs) -> TestScenario:
        """
        Читаем тест в сценарий
        """
        ...

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
