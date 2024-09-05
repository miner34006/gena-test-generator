import os.path

from jinja2 import Environment, FileSystemLoader, Template

from test_generator.library.colors import Colors
from test_generator.library.errors import ApiGenerationError
from test_generator.library.gena_data import GenaData

from .api_generator import ApiGenerator


class ApiFileUpdater(ApiGenerator):

    def __init__(self, api_template_path: str = None) -> None:
        super().__init__()
        self.template = self.__get_template(api_template_path)

    def add_api_method(self, file_path: str, gena_data: GenaData) -> str:
        print(Colors.bold('⌛  Generating api interface from swagger...'))

        with open(file_path, 'r', encoding='utf-8') as file:
            if f"def {gena_data.interface_method}(" in file.read():
                print(Colors.warning(f"⚠️ Method {gena_data.interface_method} already exists in {file_path}"))
                return gena_data.interface_method

        api_method_str = self.template.render(
            queries=gena_data.queries,
            function_params=gena_data.args + gena_data.queries,
            function_name=gena_data.interface_method,
            path=gena_data.api_path,
            method=gena_data.http_method.upper()
        )
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(api_method_str)

        print(Colors.success(f"✅  Api interface for {gena_data.http_method.upper()} {gena_data.api_path} "
              f"was generated in {file_path}"))
        return gena_data.interface_method

    def __get_template(self, template_path: str = None) -> Template:
        if template_path and not os.path.exists(template_path):
            raise ApiGenerationError(Colors.error(f"Template file not found: {template_path}"))

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
