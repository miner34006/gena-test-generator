from enum import Enum


class GenerateComponent(str, Enum):
    TESTS = 'tests'
    INTERFACE = 'interface'
    SCHEMAS = 'schemas'

    def __str__(self):
        return self.value
