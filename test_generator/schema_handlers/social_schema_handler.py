import os.path

from schemax_openapi import SchemaData

from .schema_handler import SchemaHandler


class SocialSchemaHandler(SchemaHandler):
    format_name = 'social_schema'

    __schemas_dir_path: str = ''

    def __init__(self, schemas_dir_path: str) -> None:
        super().__init__()
        self.__set_schemas_dir_path(schemas_dir_path)

    def add_schema_response(self, schema_data: SchemaData) -> None:
        print("Generating response schema from given OpenApi...")
        schema_file = f'{self.__schemas_dir_path}/{schema_data.interface_method}.py'

        with open(schema_file, 'a') as file:
            file.write(f'from d42 import optional, '
                       f'schema\n\n\n\n{schema_data.schema_prefix} = {schema_data.response_schema_d42}')

        print(f"{schema_data.http_method.upper()} {schema_data.path} response schema was generated in {schema_file}")

    def __set_schemas_dir_path(self, schemas_dir_path: str) -> None:
        if not os.path.isdir(schemas_dir_path):
            raise RuntimeError(f"'{schemas_dir_path}' doesn't exist or not a directory")
        self.__schemas_dir_path = schemas_dir_path
