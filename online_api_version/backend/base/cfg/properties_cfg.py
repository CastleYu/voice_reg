import os

from .base_cfg import BaseConfig


class PropertiesConfig(BaseConfig):
    def __init__(self, config_file_path):
        super().__init__(config_file_path)
        self.data = {}

    def _setup(self, file_path):
        """创建一个空的 Properties 文件"""
        default_data = {}
        with open(file_path, 'w', encoding='utf-8') as file:
            for key, value in default_data.items():
                file.write(f"{key}={value}\n")
        print(f"Created new properties file at {file_path}")

    def _load(self, filepath):
        """加载 Properties 配置文件"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件 {filepath} 不存在")

        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    self.data[key.strip()] = value.strip()
        self._has_set = True

    def _save(self, filepath):
        """保存 Properties 配置文件"""
        if self.data is None:
            raise ValueError("没有有效的配置数据")

        with open(filepath, 'w', encoding='utf-8') as file:
            for key, value in self.data.items():
                file.write(f"{key}={value}\n")
        self._has_set = True

    def _get(self, key: str, default=None):
        """获取指定的配置项"""
        return self.data.get(key, default)

    def _set(self, key: str, value):
        """设置指定的配置项"""
        self.data[key] = value
        return self.data

    def __str__(self):
        """返回当前 Properties 配置的字符串表示"""
        return "\n".join(f"{key}={value}" for key, value in self.data.items())

    def get(self, key: str, default=None):
        """获取指定的配置项"""
        return super().get(key, default)
