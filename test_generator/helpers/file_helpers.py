from os import listdir
from os.path import isfile, join


def get_interface_file_name(interface_dir: str) -> str:

    interface_files = [f for f in listdir(interface_dir) if
                       isfile(join(interface_dir, f)) and 'api.py' in join(interface_dir, f).lower()]

    if len(interface_files) == 0:
        raise RuntimeError(f"*Api.py files not found on {interface_dir}")

    return f'{interface_dir}/{interface_files[0]}'
