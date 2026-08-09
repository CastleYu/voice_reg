import os


class BaseConfig:
    def __init__(self, config_file_path):
        self._has_set = False
        self.path = config_file_path
        self.data = None

    def setup(self, fille_path=None):
        fille_path = fille_path or self.path
        if not os.path.exists(fille_path):
            self._setup(fille_path)

    def _setup(self, fille_path):
        raise NotImplementedError

    def load(self, load_file_path=None):
        """加载配置文件"""
        self._has_set = False
        load_file_path = self.path if load_file_path is None else load_file_path
        if not os.path.exists(load_file_path):
            self._setup(load_file_path)  # 如果没有文件则创建
        self._load(load_file_path)
        return self

    def _load(self, filepath):
        raise NotImplementedError

    def save(self, save_file_path: str = None):
        """保存配置文件"""
        if self.data is None:
            raise ValueError("没有有效的配置数据")
        save_file_path = self.path if save_file_path is None else save_file_path
        self._save(save_file_path)
        self._has_set = False
        return self

    def _save(self, filepath):
        raise NotImplementedError

    def get(self, key: str, default=None):
        """根据键获取配置项"""
        if self.data is None:
            raise ValueError("配置文件未加载")
        if self._has_set:
            self.save()
        return self._get(key, default=None)

    def _get(self, key: str, default=None):
        raise NotImplementedError

    def set(self, key: str, value: str):
        """设置配置项"""
        if self.data is None:
            raise ValueError("配置文件未加载")
        obj = self._set(key, value)
        self._has_set = True
        return obj

    def _set(self, key: str, value):
        raise NotImplementedError

    def __getattr__(self, item):
        try:
            return getattr(self.data, item)
        except AttributeError:
            return self.data.get(item)
