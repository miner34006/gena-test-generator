from json import JSONDecodeError
from typing import List

import schemax_openapi
import yaml
from schemax_openapi import SchemaData

from .swagger_handler import SwaggerHandler

from ..helpers.file_helpers import get_interface_file_name


class SwaggerYamlHandler(SwaggerHandler):
    format_name = 'swagger_handler_format'

    template_content = """
    async def $name(self, $params, locale: str = Locale.ru_RU) -> ClientResponse:
        url = self._api_url + f"$path"
        params = self._actor.params

        if locale is not None:
            params.update(locale=locale)
        return await API.$http_method(url, params=params, headers=self._actor.metadata)
        """

    def read_swagger_data(self, file_path: str, *args, **kwargs) -> List[SchemaData]:
        try:
            with open(file_path, "r") as f:
                if f.name.endswith((".yaml", ".yml")):
                    schema_data_list = schemax_openapi.collect_schema_data(yaml.load(f, yaml.FullLoader))
                else:
                    raise RuntimeError(f"'{f.name}' type is not .json or .yaml file")
                return schema_data_list
        except FileNotFoundError:
            print(f"File '{file_path}' doesn't exist")
        except JSONDecodeError:
            print(f"File '{f.name}' doesn't contain proper JSON")

    def fill_interface_template(self, schema_data: SchemaData) -> str:
        return (self.template_content.replace('$path', schema_data.path)
                                     .replace('$http_method', schema_data.http_method)
                                     .replace('$name', schema_data.interface_method)
                                     .replace('$params', ', '.join(schema_data.args)))

    def write_swagger_interface(self, interface_dir: str, file_path: str, method: str, path: str) -> None:
        print("Generating interfaces from given OpenApi...")

        interface_file_path = get_interface_file_name(interface_dir)

        data_list = self.read_swagger_data(file_path=file_path)
        data = self.__filter_schema_data_by_path_and_method(data_list, method, path)

        with open(interface_file_path, 'a', encoding='utf-8') as file:
            file.write(self.fill_interface_template(data))

        print(f"Successfully generated for {method} {path}")



    def __filter_schema_data_by_path_and_method(self, schema_data_list: List[SchemaData], method: str,
                                                path: str) -> SchemaData:
        path_data_list = list(filter(lambda data: data.path == path.lower(), schema_data_list))

        if len(path_data_list) == 0:
            raise RuntimeError(f"'{path}' doesn't exist")

        method_data_list = list(filter(lambda data: data.http_method == method.lower(), path_data_list))
        if len(method_data_list) == 0:
            raise RuntimeError(f"'{method}' for '{path}' doesn't exist")

        return method_data_list[0]
