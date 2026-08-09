import os
import time
import uuid

READ = 'read'
WRITE = 'write'


class TmpFile:
    def __init__(self, suffix='', mode='w+', dirc=None, encoding='utf-8'):
        """
        初始化临时文件类
        :param mode: 文件打开模式，默认是读写模式 (w+)
        :param suffix: 文件名的后缀，默认为空
        :param dirc: 文件保存目录，默认为当前工作目录
        """
        self.mode = mode
        self.suffix = suffix
        self.dirc = dirc or os.getcwd()  # 如果没有指定目录，使用当前工作目录
        self.path = None
        self.fp = None
        self.encoding = encoding
        # 记录读写的位置
        self.last_write_pos = 0
        self.last_read_pos = 0
        self.last_do = None
        # 使用时间戳和 uuid 生成唯一文件名
        self._generate_temp_file()

    def _generate_temp_file(self):
        """生成带有时间戳和 UUID 的临时文件名"""
        timestamp = int(time.time())
        unique_id = uuid.uuid4().hex
        file_name = f"tempfile_{timestamp}_{unique_id}{self.suffix}"
        self.path = os.path.join(self.dirc, file_name)

    def __enter__(self):
        """进入上下文时，打开文件"""
        self.fp = open(self.path, self.mode, encoding=self.encoding)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """退出上下文时，关闭文件并删除它"""
        try:
            if self.fp:
                self.fp.flush()
                self.fp.close()  # 确保文件关闭
            if os.path.exists(self.path):
                os.remove(self.path)  # 删除文件
        finally:
            try:
                if self.fp:
                    self.fp.close()
            finally:
                self.fp = None

    def write(self, data, location: int = None):
        """代理写入操作，切换到写模式并记录写位置"""
        # 切换到写模式时，保存当前的读位置, 并定位到上次写的位置
        if self.last_do == READ:
            self.last_read_pos = self.fp.tell()
            if location is None:
                self.fp.seek(self.last_write_pos)
        if location is not None:
            self.fp.seek(location)

        self.fp.write(data)
        self.fp.flush()  # 确保写入立即生效
        self.last_do = WRITE
        self.last_write_pos = self.fp.tell()

    def read(self, location: int = None):
        """代理读取操作，切换到读模式并记录读位置"""
        # 切换到读模式时，保存当前的写位置 , 并定位到上次读的位置

        if self.last_do == WRITE:

            self.last_write_pos = self.fp.tell()
            if location is None:
                self.fp.seek(self.last_read_pos)
        if location is not None:
            self.fp.seek(location)

        result = self.fp.read()
        self.last_read_pos = self.fp.tell()
        self.last_do = READ
        return result

    def __getattr__(self, item):
        # print(f'Function {item} turn to fp')
        return getattr(self.fp, item)
