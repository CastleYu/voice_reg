import json
import types


class DictEx(dict):
    def __init__(self, data=None):
        if data is None:
            data = {}
        super().__init__(data)

    def gets(self, *path):
        """
        根据给定的不定项路径获取嵌套字典或列表中的值。
        :param path: 不定项路径，可以包含 True 来遍历列表
        :return: 最终获取的值
        """
        return self._recursive_get(self, *path)

    def _recursive_get(self, current, *path):
        if not path:
            return current

        key = path[0]

        if isinstance(current, list):
            # 如果当前是列表且路径是 True，则遍历所有列表项
            if key is True:
                result = []
                for item in current:
                    result.append(self._recursive_get(item, *path[1:]))
                return result
            else:
                current = current[key]
                return self._recursive_get(current, *path[1:])
        elif isinstance(current, dict):
            if key in current:
                return self._recursive_get(current[key], *path[1:])
            else:
                raise KeyError(f"键找不到 Key '{key}' not found in dictionary.")
        else:
            raise ValueError("出现非法数据类型 Invalid path, unable to traverse further.")

    def __getitem__(self, key):
        # 使用 dict 内置的 getitem 来实现索引
        return super().__getitem__(key)

    def asdict(self):
        return dict(self)


def map_to_dict(source: dict | list | str, template: dict | list | str) -> dict | list | str:
    """
    递归地将 large_dict 中的数据映射到 template 的路径结构中
    :param source: 大的字典数据
    :param template: 预定义的小字典，定义了映射的路径结构
    :return: 返回一个映射后的字典
    """
    if isinstance(template, dict):
        mapped_dict = {}
        if not isinstance(source, (dict, list)):
            print(source, template)
            raise TypeError
        for key, value in template.items():
            if key in source:
                mapped_dict[key] = map_to_dict(source[key], value)
            else:
                mapped_dict[key] = None  # 如果大字典中没有这个路径，返回 None 或其他默认值
        return DictEx(mapped_dict)
    elif isinstance(template, list):
        if isinstance(source, list):
            return [map_to_dict(item, template[0]) for item in source]
        else:
            return []
    elif isinstance(template, types.FunctionType):
        return template(source)
    else:
        # 如果是具体的值类型，直接返回大字典中对应的值
        return source


def save_to_json(data):
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def fmt_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)
