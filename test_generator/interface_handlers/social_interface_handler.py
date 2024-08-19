import os

from schemax_openapi import SchemaData

from test_generator.interface_handlers.interface_handler import InterfaceHandler
from test_generator.library.interface_content import InterfaceContent


class SocialInterfaceHandler(InterfaceHandler):
    format_name = 'social_interface_handler'

    __interface_file_path: str = ''

    def __init__(self, interface_file_path: str) -> None:
        super().__init__()
        self.__set_interface_file_path(interface_file_path)

    def add_api_method_to_interface(self, data: SchemaData) -> None:
        print("\nGenerating interfaces from given OpenApi...")

        with open(self.__interface_file_path, 'r', encoding='utf-8') as file:
            if f"def {data.interface_method}(" in file.read():
                print(f"Method {data.interface_method} already exists in {self.__interface_file_path}, skipping...")
                return

        with open(self.__interface_file_path, 'a', encoding='utf-8') as file:
            file.write(InterfaceContent.fill_template(data))

        print(f"{data.http_method.upper()} {data.path} interface was generated in {self.__interface_file_path}")

    def __set_interface_file_path(self, interface_file_path: str) -> None:
        if not os.path.isfile(interface_file_path):
            raise RuntimeError(f"'{interface_file_path}' doesn't exist")
        self.__interface_file_path = interface_file_path
