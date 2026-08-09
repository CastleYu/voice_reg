# mymod/base/ffile/__init__.py
# 从当前包导入 metadata 和 osfile 模块
# mymod/base/ffile/__init__.py
from .metadata import *
from .osfile import *

__all__ = ['csv']
UTF = 'utf-8'
GBK = 'gbk'


def ext(filename: str) -> str:
    """Extract the file extension from a given filename."""
    return filename.rsplit('.', 1)[-1] if '.' in filename else ''


def base(filename: str) -> str:
    return filename.rsplit('.', 1)[0]


def folder_name(full_filepath: str = '') -> str:
    """从 `完整路径名` 获取文件夹名称"""
    if full_filepath:
        level = full_filepath.count('\\')
        if level >= 2:
            return full_filepath.rsplit('\\', 2)[1]
        elif level == 1:
            return full_filepath.rsplit('\\', 1)[0]
    return os.getcwd().rsplit('\\', 1)[-1]


def root(full_filepath: str = '') -> str:
    """从 `完整路径名` 获取父文件夹路径"""
    return full_filepath.rsplit('\\', 1)[0] + '\\' if full_filepath else os.getcwd()


def read_lines(path: str, codec: str = UTF) -> list:
    """从文件 `readlines` 获取行列表"""
    with open(path, 'r', encoding=codec) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def list_dir(dirc=None):
    """获取当前目录的 `listdir`"""
    if dirc is None:
        dirc = os.getcwd()
    return os.listdir(dirc)


def write_in(content: str, filepath: str = 'tempLog.txt', codec=UTF) -> None:
    """简单单次输入（覆盖）"""
    if content and content[-1] != '\n':
        content += '\n'
    with open(file=filepath, mode='w', encoding=codec) as f:
        f.write(str(content))


def write_add(content: str, filepath: str = 'tempLog.txt', codec=UTF) -> None:
    """简单追加输入"""
    if not content:
        return
    if not isinstance(content, str):
        try:
            content = str(content)
        except:
            raise TypeError
    if content[-1] != '\n':
        content += '\n'
    try:
        file = open(filepath, "r")
        file.close()
    except:
        file = open(filepath, 'w')
        file.close()
    with open(file=filepath, mode='a', encoding=codec) as f:
        f.write(str(content))
        f.close()


def name_correct(filename: str, new='', retype="noSubFolder", pat="") -> str:
    """
    修正文件名中的特定字符，使其在不同场景下更为合适。

    参数:
    - filename (str): 原始文件名。
    - new (str): 用于替换非法字符的字符，默认为空。
    - retype (str): 选择文件名修正模式。默认为 "noSubFolder"。
        "noSubFolder": 替换可能在子文件夹名中的非法字符。
        "obsidian": 在 "noSubFolder" 的基础上，还替换 Obsidian 笔记软件中会导致问题的字符，如 "#", "[", "]", "^"。
        "webdav": 在 "obsidian" 的基础上，还替换 WebDAV 云同步中会导致问题的字符，如 "&?#<>+%/"。

    返回:
    - str: 修正后的文件名。

    示例:
    >>> name_correct("example\\name?.txt", retype="noSubFolder")
    "examplename.txt"
    
    >>> name_correct("example[name].txt", retype="obsidian")
    "examplename.txt"
    """
    import re
    # 替换换行符为下划线
    filename = re.sub(r'\n', '_', filename)

    # 替换不后跟反斜杠的冒号和其他非法字符
    filename = re.sub(r'(:(?!\\)|[*?<>|"\r\t\b\f\x00-\x1f])', new, filename)

    if not pat:
        filename = re.sub(r'(\\/)', new, filename)
    # 如果type为"noSubFolder"，替换文件路径的分隔符
    if retype == "noSubFolder":
        filename = re.sub(r'(\\/)', new, filename)
    # 如果type为"obsidian"，替换"#","[","]","^"等字符
    elif retype == "obsidian":
        filename = re.sub(r'(\\/)', new, filename)
        filename = re.sub(r'([#\[\]^%])', new, filename)
    elif retype == 'webdav':
        filename = re.sub(r'(\\/)', new, filename)
        filename = re.sub(r'([#\[\]^])', new, filename)
        filename = re.sub(r'[&?#<>+%/]', new, filename)
    return filename
