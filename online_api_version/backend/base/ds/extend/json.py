import ast
import importlib
import json
import traceback
from typing import Optional, Type, TypeVar, Any

from dacite import from_dict, ForwardReferenceError, UnexpectedDataError, WrongTypeError, \
    MissingValueError, DaciteFieldError
from dacite.dataclasses import DefaultValueNotFoundError
from pandas.errors import MergeError
from typing_extensions import Self

from .kv import InvalidOpError, KVNode
from ._imports import *

T = TypeVar("T")


class JsonNode(KVNode):
    def __init__(self, key, value):
        super().__init__(key, value)
        self._type_check()  # 检查对应类型

    def _type_check(self):
        raise NotImplementedError

    def get(self, key, default=None) -> Self:
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def build(self, key, value: Any):
        """根据数据类型构建相应的JsonNode实例"""
        if isinstance(value, dict):
            return JsonObject(key, value)
        elif isinstance(value, list):
            return JsonArray(key, value)
        elif isinstance(value, (int, float, str, type(None))):
            return JsonAtom(key, value)
        elif isinstance(value, self.__class__):
            return value
        else:
            raise TypeError(f"无法根据类型 {type(value).__class__} 创建 JsonNode 实例")

    def _invalid_key_error(self, key):
        raise KeyError(f"尝试在({self.key}: {self.__class__})中获取非法索引[{key}: {type(key).__class__}]")


class JsonArray(JsonNode):
    """列表类型"""
    value: list[JsonNode]

    def __init__(self, key, value):
        super().__init__(key, value)
        self._type_check()

    def _type_check(self):
        assert isinstance(self.value, list)

    def _get(self, index):
        value = self.value[index]
        # if isinstance(value, JsonAtom):
        #     return value.value
        return value

    def get(self, index: int, default: Any = None):
        try:
            return self._get(index)
        except IndexError:
            return default

    def __getattr__(self, item):
        if item in ('key', 'value', 'type'):
            return super().__getattribute__(item)
        self._invalid_key_error(item)

    def __getitem__(self, index):
        try:
            return self.value[index]
        except:
            traceback.print_exc()
            self._invalid_key_error(index)

    def set(self, index: int, value):
        """设置指定索引的值"""
        try:
            self.value[index] = self.build(index, value)
        except:
            if index == len(self.value):
                self.add(value)
            traceback.print_exc()
            self._invalid_key_error(index)

    def __setitem__(self, index, value):
        """通过索引设置值"""
        self.set(index, value)

    def __delitem__(self, index):
        """删除指定索引的项"""
        try:
            del self.value[index]
        except:
            traceback.print_exc()
            self._invalid_key_error(index)

    def add(self, value):
        key = len(self.value)
        self.value.append(self.build(key, value))

    def __add__(self, other):
        """拼接迭代对象；追加元素值"""
        value = self.value.copy()
        if isinstance(other, self.__class__):
            value.extend(other.value)
        elif isinstance(other, list):
            for index, item in enumerate(other, start=len(self.value)):
                value.append(self.build(index, item))
        else:
            value.append(self.build(len(self.value), other))
        return self.__class__(self.key, value)

    # def __iadd__(self, other):
    #     """拼接迭代对象；追加元素值"""
    #     if isinstance(other, self.__class__):
    #         self.value.extend(other.value)
    #     elif isinstance(other, list):
    #         for index, item in enumerate(other, start=len(self.value)):
    #             self.value.append(self.build(index, item))
    #     else:
    #         self.value.append(other)
    #     return self

    def __sub__(self, other):
        """按值删除元素(仅一次)"""
        value = self.value.copy()
        if isinstance(other, (self.__class__, list)):
            [value.remove(i) for i in other if i in value]
        elif other in value:
            value.remove(other)
        return self.__class__(self.key, value)

    def __mul__(self, other):
        """笛卡尔积；列表重复"""
        if isinstance(other, (self.__class__, list)):
            return self.__class__(self.key, [[a * b for b in other] for a in self])
        elif isinstance(other, int):
            return self.__class__(self.key, self.value * other)
        raise InvalidOpError(self, other, self.key)

    def __truediv__(self, other):
        """删除末尾的n个元素"""
        if isinstance(other, int):
            return self.__class__(self.key, self.value[:-other])
        raise InvalidOpError(self, other, self.key)

    def __rtruediv__(self, other):
        """删除开始的n个元素"""
        if isinstance(other, int):
            return self.__class__(self.key, self.value[other:])
        raise InvalidOpError(self, other, self.key)

    def __mod__(self, other):
        """保留末尾的n个元素"""
        if isinstance(other, int):
            return self.__class__(self.key, self.value[-other:])
        raise InvalidOpError(self, other, self.key)

    def __rmod__(self, other):
        """保留开始的n个元素"""
        if isinstance(other, int):
            return self.__class__(self.key, self.value[:other])
        raise InvalidOpError(self, other, self.key)

    def __floordiv__(self, other):
        raise InvalidOpError(self, other, self.key)

    def __and__(self, other):
        """取所有为n的元素(列表：逐个)"""
        if isinstance(other, (self.__class__, list)):
            return self.__class__(self.key, [i for i in self if i in other])
        else:
            return self.__class__(self.key, [i for i in self if i == other])

    def __or__(self, other):
        """存在值为n的元素(列表：逐个)"""
        if isinstance(other, (self.__class__, list)):
            return ...
        else:
            return any(i == other for i in self)

    def __xor__(self, other):
        """取所有不为n的元素(列表：逐个) | 按值删除元素(所有)"""
        if isinstance(other, (self.__class__, list)):
            return self.__class__(self.key, [i for i in self if i not in other])
        else:
            return self.__class__(self.key, [i for i in self if i != other])

    def __invert__(self):
        """取反转的列表"""
        self.value = self.value[::-1]
        return self

    def __lshift__(self, other):
        """将所有元素移动n个单位，溢出位置回到另一端"""
        if isinstance(other, int):
            n = other % self.__len__()
            return self.__class__(self.key, self.value[n:] + self.value[:n])
        raise InvalidOpError(self, other, self.key)

    def __rshift__(self, other):
        """将所有元素移动n个单位，溢出位置回到另一端"""
        if isinstance(other, int):
            n = other % self.__len__()
            return self.__class__(self.key, self.value[-n:] + self.value[:-n])
        raise InvalidOpError(self, other, self.key)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        elif isinstance(other, list):
            return self.value == other
        return all(x == other for x in self.value)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.value < other.value
        elif isinstance(other, list):
            return self.value < other
        return all(x < other for x in self.value)

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.value <= other.value
        elif isinstance(other, list):
            return self.value <= other
        return all(x <= other for x in self.value)

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.value > other.value
        elif isinstance(other, list):
            return self.value > other
        return all(x > other for x in self.value)

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.value >= other.value
        elif isinstance(other, list):
            return self.value >= other
        return all(x >= other for x in self.value)

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.value != other.value
        elif isinstance(other, list):
            return self.value != other
        return any([x != other for x in self.value])

    def __contains__(self, item):
        return item in self.value


class JsonObject(JsonNode):
    value: dict[str, JsonNode]

    def __init__(self, key, value):
        super().__init__(key, value)
        self._type_check()

    def _type_check(self):
        assert isinstance(self.value, dict)

    def _get(self, key, default):
        value = self.value.get(key, default)
        # if isinstance(value, JsonAtom):
        #     return value.value
        return value

    def get(self, key, default: Any = None):
        return self._get(key, default)

    def __getattr__(self, item):
        if item in ('key', 'value', 'type'):
            return super().__getattribute__(item)
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def set(self, key, value):
        """设置指定键的值"""
        self.value[key] = self.build(key, value)

    def __setitem__(self, key, value):
        self.set(key, value)

    def delete(self, key):
        try:
            del self.value[key]
        except KeyError:
            raise KeyError(f"键 {key} 不存在，无法删除")

    def __delitem__(self, key):
        self.delete(key)

    def __setattr__(self, key, value):
        if key in ('key', 'value', 'type') and not hasattr(self, key):
            super().__setattr__(key, value)
            return
        self.set(key, value)

    def add(self, key, value):
        if key not in self.value:
            self.value[key] = self.build(key, value)
        else:
            raise KeyError(f"键 {key} 已存在，无法添加，请使用set(key,value)")

    def __add__(self, other):
        value = self.value.copy()
        if isinstance(other, self.__class__):
            value.update(other.value)
        elif isinstance(other, dict):
            value.update(other)
        elif isinstance(other, JsonNode):
            # elif isinstance(other, self.__class__.mro()[-2]):
            value[other.key] = other
        else:
            raise InvalidOpError(self, other, self.key)
        return self.__class__(self.key, value)

    # def __iadd__(self, other):
    #     if isinstance(other, self.__class__):
    #         self.value.update(other.value)
    #     elif isinstance(other, dict):
    #         # self.value.update(other)
    #         raise NotImplementedError
    #     elif isinstance(other, JsonNode):
    #         self.value[other.key] = other
    #     else:
    #         raise InvalidOpError(self, other, self.key)
    #     return self

    def __sub__(self, other):
        value = self.value.copy()
        if isinstance(other, self.__class__):
            value = {k: v for k, v in self if other.value.get(k) != v}
        elif isinstance(other, dict):
            value = {k: v for k, v in self if other.get(k) != v}
        elif isinstance(other, JsonNode):
            value.pop(other.key, None)
        else:
            raise InvalidOpError(self, other, self.key)
        return self.__class__(self.key, value)

    def __mul__(self, other):
        """取交集(同键)"""
        if isinstance(other, (self.__class__, dict)):
            # or getitem iter
            return self.__class__(self.key, {key: other[key] for key in self | other})
        elif isinstance(other, (JsonArray, list)):
            # in getitem iter
            return self.__class__(self.key, {key: self[key] for key in other if key in self})
        elif isinstance(other, JsonAtom):
            if other.key not in self:
                return other
            return JsonAtom(other.key, self.get(other.key))
        raise InvalidOpError(self, other, self.key)

    def __pow__(self, power, modulo=None):
        """取交集(同键同值)"""
        if isinstance(power, (self.__class__, dict)):
            # or getitem iter
            return self.__class__(self.key, {k: v for k, v in self if self[k] == v})
        # elif isinstance(power, (JsonArray, JsonAtom)):
        #     # in getitem iter
        #     return power.__class__(power.key, self.value.get(power.key) or power.value)
        raise InvalidOpError(self, power, self.key)

    def __truediv__(self, other):
        """去除同键"""
        if isinstance(other, (self.__class__, dict, JsonArray, list)):
            return self.__class__(self.key, {k: v for k, v in self if k in other})
        else:
            value = self.value.copy()
            if isinstance(other, JsonAtom):
                value.pop(other.key, None)
            else:
                value.pop(other, None)
            return self.__class__(self.key, value)

    def __floordiv__(self, other):
        return self.__sub__(other)

    def __mod__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return self.__class__(self.key, {k: other.get(k, self.get(k)) for k in self.keys() ^ other.keys()})
        raise InvalidOpError(self, other, self.key)

    def __and__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return self.keys() == other.keys()
        elif isinstance(other, (JsonArray, list)):
            return list(self.keys()) == list(other)
        return False
        # raise InvalidOpError(self, other, self.key)

    def __or__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return self.keys() | other.keys()
        elif isinstance(other, (JsonArray, list)):
            return self.keys() | list(other)
        elif isinstance(other, JsonNode):
            return self.keys() | [other.key]
        else:
            return self.keys() | [other]

    def __invert__(self):
        """所有值都为空"""
        return self.value == {} or all(not value for value in self.value.values())

    def __xor__(self, other):
        """键交集"""
        if isinstance(other, (self.__class__, dict)):
            return self.keys() & other.keys()
        elif isinstance(other, (JsonArray, list)):
            return self.keys() & other.keys()
        elif isinstance(other, JsonNode):
            return self.keys() & [other.key]
        else:
            return self.keys() & [other]

    def __lt__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return set(self.keys()) < set(other.keys())
        raise InvalidOpError(self, other, self.key)

    def __le__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return set(self.keys()) <= set(other.keys())
        raise InvalidOpError(self, other, self.key)

    def __gt__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return set(self.keys()) > set(other.keys())
        raise InvalidOpError(self, other, self.key)

    def __ge__(self, other):
        if isinstance(other, (self.__class__, dict)):
            return set(self.keys()) >= set(other.keys())
        raise InvalidOpError(self, other, self.key)

    def __iter__(self):
        return self.value.items()

    def __contains__(self, item):
        if isinstance(item, JsonNode):
            return item.key in self.value and item.value == self.value[item.key]
        else:
            return item in self.value

    def __str__(self):
        return json.dumps(JsonParser().to_json(self), ensure_ascii=False, indent=4)

    def __repr__(self):
        return json.dumps(JsonParser().to_json(self), ensure_ascii=False, indent=4)

    def keys(self):
        return self.value.keys()


class JsonAtom(JsonNode):
    value: int | float | None | str

    def __init__(self, key, value):
        super().__init__(key, value)
        self._type_check()

    def _type_check(self):
        assert isinstance(self.value, (int, float, type(None), str, bool))

    def _invalid_key_error(self, key):
        raise TypeError(f"key({self.key}) = value({self.value}) 已是原子键值对(在获取 key({key}) 时)")

    def get(self, *args):
        return self.value

    def __getitem__(self, item):
        return self.value[item]

    def set(self, value, *args):
        self.value = value


class JsonParser:
    def __init__(self):
        pass

    def parse(self, data: Any, key="") -> JsonObject | JsonAtom | JsonArray:
        """
        解析 JSON 数据，并根据其类型返回对应的 JsonNode 对象。
        """
        if isinstance(data, dict):
            return JsonObject(key, {k: self.parse(v, k) for k, v in data.items()})
        elif isinstance(data, list):
            return JsonArray(key, [self.parse(item, str(index)) for index, item in enumerate(data)])
        elif isinstance(data, (int, float, str, type(None))):
            return JsonAtom(key, data)
        else:
            raise TypeError(f"不支持的数据类型 {type(data)}")

    def from_file(self, json_str: str) -> JsonObject:
        """
        将 JSON 字符串解析为 JsonNode 对象。
        """
        data = json.loads(json_str)
        return self.parse(data)

    def to_json(self, node: JsonNode) -> Any:
        """
        将 JsonNode 对象转换为原始的 JSON 数据（字典、列表或基本类型）。
        """
        if isinstance(node, JsonObject):
            return {key: self.to_json(value) for key, value in node.value.items()}
        elif isinstance(node, JsonArray):
            return [self.to_json(item) for item in node.value]
        elif isinstance(node, JsonAtom):
            return node.value
        else:
            raise TypeError(f"不支持的 JsonNode 类型 {type(node)}")

    def build_dto(self, data_class: Type[T], data: dict) -> Optional[T]:
        """从字典安全创建数据类实例，捕获异常并提供中文提示。"""
        try:
            return from_dict(data_class, data)
        except ForwardReferenceError as e:
            print(f"原始数据: {data}")
            print(f"错误提示: 前向引用错误 - {str(e)}")
        except UnexpectedDataError as e:
            print(f"原始数据: {data}")
            print(f"错误提示: 输入数据中有未期望的字段: {e.keys}")
        except WrongTypeError as e:
            print(f"原始数据: {data}")
            print(f"错误提示: 字段 '{e.field_path}' 的值类型错误，期望类型: {e.field_type}, 实际值: {e.value}")
        except MissingValueError as e:
            print(f"原始数据: {data}")
            print(f"错误提示: 字段 '{e.field_path}' 缺失，且无法找到默认值")
        except DaciteFieldError as e:
            print(f"原始数据: {data}")
            print(f"错误提示: 字段处理失败，字段路径: {e.field_path}")
        except DefaultValueNotFoundError as e:
            print(f"原始数据: {data}")
            print(f"错误提示: 字段无法找到默认值，错误信息: {str(e)}")
        except Exception as e:
            print(f"原始数据: {data}")
            print(f"未知错误: {str(e)}")
        return None

    def gen_dto(self, root_name: str, json_dict: dict, direc=None):
        """根据JSON数据结构动态生成DTO类并返回实例化对象"""
        if isinstance(json_dict, list):
            return self.gen_dto(root_name, json_dict[0], direc)
        root_name = to_snake_case(root_name)
        cb_lst = []
        cls_name = to_pascal_case(root_name)
        cb = ClassBuilder(cls_name)

        def handle_dict(key: str, dic: Any):
            """处理字典类型，生成嵌套数据类"""
            cls_name = to_pascal_case(key)
            sub_cb = ClassBuilder(cls_name)
            for k, v in dic.items():
                annote = handle(k, v)
                try:
                    sub_cb.add_body(AnnAssignBuilder().set(k).as_type(annote).build())
                except ValueError:
                    k_ = k + '_'
                    sub_cb.add_body(AnnAssignBuilder().set(k_).as_type(annote).build())
            sub_cb.add_decorator(VarBuilder("dataclass").build())
            cb_lst.append(sub_cb.build())
            return cls_name

        def handle_list(key: str, lst: Any):
            """处理列表类型，自动检测元素类型"""
            container = Any
            if isinstance(lst[0], dict):
                dic = {}
                for item in lst:
                    dic.update(item)
                container = handle_dict(key, dic)
            else:
                container = handle(key, lst[0])
            return VarBuilder('list').get(var=container).build()

        def handle(key: str, value: Any) -> str:
            """类型分发处理核心逻辑"""
            type_ = "Any"
            if isinstance(value, str):
                type_ = 'str'
            elif isinstance(value, int):
                type_ = "int"
            elif isinstance(value, float):
                type_ = "float"
            elif isinstance(value, bool):
                type_ = "bool"
            elif isinstance(value, list):
                type_ = handle_list(key, value)
            elif isinstance(value, dict):
                type_ = handle_dict(key, value)
            return VarBuilder("Optional").get(var=type_).build()

        cb.add_decorator(VarBuilder("dataclass").build())
        for k, v in json_dict.items():
            annote = handle(k, v)
            try:
                cb.add_body(AnnAssignBuilder().set(k).as_type(annote).build())
            except ValueError:
                k += "_"
                cb.add_body(AnnAssignBuilder().set(k).as_type(annote).build())
        cb_lst.append(cb.build())

        module = ast.Module(
            body=[
                ast.ImportFrom(module="dataclasses", names=[ast.alias(name="dataclass")], level=0),
                ast.ImportFrom(module="typing", names=[ast.alias(name="Any"), ast.alias(name="Optional")], level=0),
                *cb_lst
            ]
        )

        module_name = root_name + "_dto"
        file_name = module_name + ".py"
        if direc is None:
            with open(file_name, "w", encoding="utf-8") as f:
                code = CodeGenerator.to_code(module)
                f.write(code)
            module_obj = importlib.import_module(module_name)
            return self.build_dto(getattr(module_obj, cls_name), json_dict)
        else:
            import os
            os.makedirs(direc, exist_ok=True)
            full_path = os.path.join(direc, file_name)
            with open(full_path, "w", encoding="utf-8") as f:
                code = CodeGenerator.to_code(module)
                f.write(code)

            module_dir = os.path.abspath(direc)
            import sys
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)

            try:
                module_obj = importlib.import_module(module_name)
                if module_dir in sys.path:
                    sys.path.remove(module_dir)
                return self.build_dto(getattr(module_obj, cls_name), json_dict)
            finally:
                if module_dir in sys.path:
                    sys.path.remove(module_dir)


def json_to_template(json_text):
    # 解析 JSON 文本为字典
    if isinstance(json_text, str):
        data = json.loads(json_text)
    elif isinstance(json_text, dict):
        data = json_text
    else:
        raise ValueError("Input must be a JSON string or a dictionary.")

    def replace_with_placeholders(obj):
        if isinstance(obj, dict):
            # 对于字典，递归处理其值
            return {k: replace_with_placeholders(v) if isinstance(v, (dict, list)) else "${%s}" % k for k, v in
                    obj.items()}
        elif isinstance(obj, list):
            # 对于列表，将所有元素合并为一个元素
            merged_element = {}
            for elem in obj:
                if not isinstance(elem, dict):
                    raise MergeError(f"列表中的元素必须是字典，而不是 {type(elem)}")  # TODO 解决常规列表类型
                for k, v in elem.items():
                    if k in merged_element:
                        if isinstance(merged_element[k], dict) and isinstance(v, dict):
                            merged_element[k] = {**merged_element[k], **v}
                        elif type(merged_element[k]) is not type(v):
                            raise MergeError(f"键 '{k}' 的值类型冲突：{type(merged_element[k])} 和 {type(v)}")
                    else:
                        merged_element[k] = v
            return [replace_with_placeholders(merged_element)]
        else:
            # 其他类型，直接返回
            return obj

    # 生成模板数据
    template_data = replace_with_placeholders(data)
    # 将模板数据转换为格式化的 JSON 字符串
    template_json = json.dumps(template_data, ensure_ascii=False, indent=2)
    return template_json
