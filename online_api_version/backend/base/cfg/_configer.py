from base.ddir import *
from .json_cfg import JsonConfig
from .properties_cfg import PropertiesConfig

__all__ = ['Configer',
           'JsonConfig',
           "PropertiesConfig"]


class Configer:
    def __init__(self, config_file_path, core=JsonConfig):
        self.path = DiskPath(config_file_path).abs_path
        self.core = core(self.path)
        self.load()

    def load(self, file_path=None):
        return self.core.load(file_path or self.path)
