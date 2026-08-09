from .base_cfg import *
from ..ds.extend.json import *


class JsonConfig(BaseConfig):
    parser: JsonParser
    data: JsonObject

    def __init__(self, config_file_path):
        super().__init__(config_file_path)
        self.parser = JsonParser()

    def _setup(self, fille_path):
        default_data = {}
        with open(fille_path, 'w', encoding='utf-8') as file:
            json.dump(default_data, file, ensure_ascii=False, indent=4)

    def _load(self, filepath):
        """加载配置文件"""
        with open(filepath, 'r', encoding='utf-8') as file:
            json_str = file.read()
        self.data = self.parser.from_file(json_str)
        self._has_set = True

    def _save(self, filepath):
        """保存配置文件"""
        json_str = json.dumps(self.parser.to_json(self.data), ensure_ascii=False, indent=4)
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json_str)
        self._has_set = True

    def _get(self, key: str, default=None) -> JsonNode:
        """获取配置项"""
        return self.data.get(key, default)

    def _set(self, key: str, value: Any):
        """设置配置项"""
        self.data[key] = value
        return self.data

    def __str__(self):
        return str(self.data)

    # Signature fix
    def get(self, key: str, default=None) -> JsonNode:
        return super().get(key, default)
