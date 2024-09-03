import os.path

from ..library.colors import Colors
from ..library.gena_data import GenaData
from .schema_generator import SchemaGenerator


class SchemaFileCreator(SchemaGenerator):

    def generate_response_schema(self, schemas_dir: str, gena_data: GenaData) -> str | None:
        print(Colors.bold("⌛  Generating response schema from swagger..."))

        schema_file = f'{schemas_dir}/{gena_data.interface_method}.py'

        if os.path.exists(schema_file):
            print(Colors.warning(f"⚠️ File with response schema already exists: {schema_file}"))
            return

        with open(schema_file, 'a') as file:
            file.write(f'from d42 import optional, '
                       f'schema\n\n\n\n{gena_data.response_schema_name} = {gena_data.response_schema}')

        print(Colors.success(f"✅  Response schema for {gena_data.response_schema_name} "
              f"was generated in {schema_file}"))
        return gena_data.response_schema_name
