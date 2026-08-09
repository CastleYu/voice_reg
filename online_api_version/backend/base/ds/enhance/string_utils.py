import re


def find_urls(text):
    # 更精确的匹配URL的正则表达式模式
    url_pattern = re.compile(
        r'(https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))'
    )

    # 使用re.findall()函数来查找所有符合模式的URL
    urls = url_pattern.findall(text)

    return urls


def is_file_url(url):
    # 常见文件扩展名列表
    file_extensions = (
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.zip', '.rar',
        '.tar', '.gz', '.7z', '.mp3', '.mp4', '.avi', '.mov',
        '.mkv', '.wav', '.flac', '.txt', '.csv', '.json', '.xml',
        '.html', '.htm', '.css', '.js', '.exe', '.dll', '.iso', 'bin', 'm4v'
    )

    # 匹配URL结尾的文件扩展名
    pattern = r'({})$'.format('|'.join(re.escape(ext) for ext in file_extensions))

    return re.search(pattern, url) is not None


def check_string(string):
    def is_url(string):
        # 正则表达式匹配 URL
        url_pattern = re.compile(
            r'^(https?|ftp):\/\/'  # 协议 http:// 或 https:// 或 ftp://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # 域名
            r'localhost|'  # 或 localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # 或 IP 地址
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # 或 IPv6 地址
            r'(?::\d+)?'  # 端口号
            r'(?:\/?|[\/?]\S+)$', re.IGNORECASE)

        return re.match(url_pattern, string) is not None

    def is_file_path(string):
        # 判断是否是文件路径
        # Windows 系统文件路径通常以驱动器符号 (C:\) 开头
        # Unix 或 Linux 系统文件路径通常以 / 开头
        import os
        if os.path.isabs(string):
            return True

        # 检查是否包含文件扩展名
        if os.path.splitext(string)[1] != '':
            return True

        return False

    if is_url(string):
        return "url"
    elif is_file_path(string):
        return "filepath"
    else:
        return "unknow"


def safe_url_join(base, path, default_scheme='http'):
    from urllib.parse import urlparse, urljoin
    # 如果 base 为 None，检查 path 是否为完整的 URL
    if base is None:
        parsed_path = urlparse(path)
        if parsed_path.scheme and parsed_path.netloc:
            return path
        else:
            raise ValueError(f"`{path}` is not a complete URL, and `base` is None.")

    # 如果 base 没有包含 scheme，自动加上默认的 scheme
    if '://' not in base:
        base = f"{default_scheme}://{base}"

    # 解析基础URL并分解出路径部分
    parsed_base = urlparse(base)
    base_path = parsed_base.path

    # 确保基础路径和新路径之间有一个斜杠
    if not base_path.endswith('/'):
        base_path += '/'

    # 处理路径组合，确保不丢失基础路径
    combined_path = urljoin(base_path, path.lstrip('/'))

    # 构造完整的URL
    full_url = f"{parsed_base.scheme}://{parsed_base.netloc}{combined_path}"
    return full_url


def remove_html_tags(text):
    # 定义一个正则表达式模式，用于匹配HTML标签
    html_tag_pattern = re.compile(r'\s*<.*?>\s*')

    # 使用sub函数替换所有匹配到的HTML标签为空字符串
    clean_text = re.sub(html_tag_pattern, '', text)

    return clean_text


def is_valid_url(url):
    """
    判断输入的字符串是否是一个合法的URL，而不是仅仅是一个路径。

    :param url: 待检查的URL字符串
    :return: 如果是合法的URL返回True，否则返回False
    """
    try:
        # 解析URL
        from urllib.parse import urlparse
        parsed_url = urlparse(url)

        # 检查是否有合法的scheme（例如http或https）和netloc（主机名）
        return all([parsed_url.scheme, parsed_url.netloc])
    except ValueError:
        # 如果解析URL时发生错误，则说明不是合法的URL
        return False


def simplify(zh_tw):
    import opencc
    converter = opencc.OpenCC('t2s')
    simplified_text = converter.convert(zh_tw)
    return simplified_text


def fix_filename(filename):
    # 定义 Windows 不允许的文件名中的非法字符
    invalid_characters = r'[<>:"/\\|?*]'

    # Windows 保留的特殊文件名
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }

    # 1. 移除非法字符
    filename = re.sub(invalid_characters, '', filename)

    # 2. 去除文件名末尾的空格和句点
    filename = filename.rstrip(' .')

    # 3. 检查并修正保留的文件名
    name, ext = filename.split('.', 1) if '.' in filename else (filename, '')
    if name.upper() in reserved_names:
        name += '_fixed'  # 加一个后缀，避免使用保留名

    # 4. 重新组合文件名和扩展名
    if ext:
        filename = f"{name}.{ext}"
    else:
        filename = name

    return filename


def str_remove(s: str, *remove_strs) -> str:
    for r in remove_strs:
        s = s.replace(r, '')
    return s


def clean_str(s):
    if isinstance(s, (list, tuple)):
        # 递归处理列表或元组，同时去除 None
        return type(s)(clean_str(item) for item in s if item is not None)
    elif s is None or not isinstance(s, str):
        # 如果 s 是 None，返回空字符串；如果不是字符串且不为 None，直接返回
        return '' if s is None else s
    # 去除字符串首尾的换行符和空格，并移除内部的 '\n' 和 '\r'
    s = s.strip("\n\r ")
    s = str_remove(s, '\n', '\r')
    return s
