from abc import ABC, abstractmethod

from test_generator.library.scenario import TestScenario
from test_generator.library.suite import Suite


class BaseReader(ABC):
    name = 'AbstractBaseReader'

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
