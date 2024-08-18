from abc import ABC, abstractmethod

from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite


class TestHandler(ABC):
    name = 'AbstractTestHandler'

    @abstractmethod
    def read_test(self, file_path: str, *args, **kwargs) -> tuple[str, str, TestScenario | None]:
        """
        Читаем тест в объект сценария
        """
        ...

    @abstractmethod
    def read_tests(self, target_dir: str, *args, **kwargs) -> Suite:
        """
        Читаем тесты в съют
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
