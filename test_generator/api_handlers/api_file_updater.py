import os.path

import schemax_openapi
import yaml
from jinja2 import Environment, FileSystemLoader, Template
from schemax_openapi import SchemaData

from test_generator.library.errors import ApiGenerationError

from .api_generator import ApiGenerator


class ApiFileUpdater(ApiGenerator):
    yaml_file_path: str = ''

    def __init__(self, yaml_file_path: str, api_template_path: str = None) -> None:
        super().__init__()
        self.__set_yaml_file(yaml_file_path)
        self.template = self.__get_template(api_template_path)

    def add_api_method(self, file_path: str, method: str, path: str) -> str:
        if not os.path.exists(file_path):
            raise ApiGenerationError(f"'{file_path}' doesn't exist")

        print("\n⌛ Generating api interface from swagger...")
        data_list = self.__read_swagger_data()
        data = self.__filter_schema_data_by_path_and_method(data_list, method, path)

        with open(file_path, 'r', encoding='utf-8') as file:
            if f"def {data.interface_method}(" in file.read():
                print(f"⚠️ Method {data.interface_method} already exists in {file_path}\n")
                return data.interface_method

        api_method_str = self.template.render(
            queries=data.queries,
            function_params=data.args + data.queries,
            function_name=data.interface_method,
            path=path,
            method=method.upper()
        )
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(api_method_str)

        print(f"✅ {method} {path} interface was generated in {file_path}\n")
        return data.interface_method

    def __read_swagger_data(self) -> list[SchemaData]:
        with open(self.yaml_file_path, "r") as f:
            schema_data_list = schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))
            return schema_data_list

    def __filter_schema_data_by_path_and_method(self, schema_data_list: list[SchemaData], method: str,
                                                path: str) -> SchemaData:
        path_data_list = list(filter(lambda data: data.path == path.lower(), schema_data_list))

        if len(path_data_list) == 0:
            raise ApiGenerationError(f"'{path}' doesn't exist")

        method_data_list = list(filter(lambda data: data.http_method == method.lower(), path_data_list))
        if len(method_data_list) == 0:
            raise ApiGenerationError(f"'{method}' for '{path}' doesn't exist")

        return method_data_list[0]

    def __set_yaml_file(self, yaml_file_path: str) -> None:
        if not os.path.exists(yaml_file_path):
            raise ApiGenerationError(f"'{yaml_file_path}' doesn't exist")
        self.yaml_file_path = yaml_file_path

    def __get_template(self, template_path: str = None) -> Template:
        if template_path and not os.path.exists(template_path):
            raise ApiGenerationError(f"Template file not found: {template_path}")

        if not template_path:
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
            template_path = f'{templates_dir}/api_template.jinja'

        template_dir = os.path.dirname(template_path)
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template_name = os.path.basename(template_path)
        return env.get_template(template_name)
