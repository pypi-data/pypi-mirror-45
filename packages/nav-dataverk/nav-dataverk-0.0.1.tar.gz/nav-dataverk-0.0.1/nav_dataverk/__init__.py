from . import connectors
from . import utils
from nav_dataverk.context.settings import singleton_settings_store_factory
from nav_dataverk.api import _current_dir, read_sql, to_sql, write_notebook, read_kafka
from nav_dataverk.dataverk_context import DataverkContext
from nav_dataverk.dataverk import Dataverk
from pathlib import Path

version_file_path = Path(__file__).parent.joinpath("VERSION")
with version_file_path.open("r") as fh:
    __version__ = fh.read()

__all__ = ['connectors',
           '_current_dir',
           'read_sql',
           'to_sql',
           'utils',
           'write_notebook',
           'Dataverk',
           'DataverkContext',
           'singleton_settings_store_factory',
           'read_kafka'
           ]
