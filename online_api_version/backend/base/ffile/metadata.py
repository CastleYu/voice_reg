import os
import time

from base.logs import ConsoleLog


class Metadata(ConsoleLog):
    UNKNOW = -1

    def __init__(self, path=None, **kwargs):
        super().__init__()
        self.debug = False  # 调试标识
        self.path = path if path is not None else kwargs.get('path', '')  # 路径
        self.folder = ''  # 文件夹（绝对）
        self.title = ''  # 文件名
        self.extension = ''  # 扩展名
        self.size: int = self.UNKNOW  # 文件大小
        self.mtime: int = self.UNKNOW  # 修改时间
        if kwargs:
            for key, value in kwargs.items():
                if key != 'path':
                    setattr(self, key, value)
        if self._build_metadata():
            self._suc_log("Metadata built successfully")
        else:
            self._warn_log("Path is empty, built an empty metadata")

    def _build_metadata(self):
        if not self.path:
            return False
        if not os.path.exists(self.path):
            raise FileNotFoundError("未找到文件")
        if not os.path.isfile(self.path):
            raise IsADirectoryError("目标是一个文件夹而非文件")
        self._parse_file_path()
        self._update_metadata()
        return True

    def _update_metadata(self):
        if os.path.isfile(self.path):
            self.size = os.path.getsize(self.path)
            self.mtime = os.path.getmtime(self.path)

    def _parse_file_path(self):
        if isinstance(self.path, str) and self.path and os.path.isfile(self.path):
            self.path = os.path.abspath(self.path)
            self.folder = os.path.dirname(self.path)
            self.title, ext = os.path.splitext(os.path.basename(self.path))
            self.extension = ext.lstrip('.')

    @property
    def file_name(self):
        return self.title

    @file_name.setter
    def file_name(self, file_name):
        self.title = file_name

    @property
    def file_type(self):
        return self.extension

    @file_type.setter
    def file_type(self, file_type):
        self.extension = file_type

    def __str__(self):
        if not self.path:
            print("\n{}: 正在尝试输出一个空的文件信息\n".format(self.__class__.__name__))
        modified_time = "Unknown" if self.mtime == self.UNKNOW else time.ctime(self.mtime)
        return (f"Path: {self.path}\n"
                f"Folder: {self.folder}\n"
                f"Title: {self.title}\n"
                f"Extension: {self.extension}\n"
                f"Size: {self.size}\n"
                f"Modified Time: {modified_time}")
