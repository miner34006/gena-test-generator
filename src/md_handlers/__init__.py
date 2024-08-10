from .md_handler import MdHandler
from .md_list_handler import MdListHandler


def get_md_handlers() -> list[MdHandler]:
    return [f() for f in MdHandler.__subclasses__()]


def get_default_md_handler() -> MdHandler:
    return MdListHandler()