import os
import re
from typing import List, Dict

from bs4 import BeautifulSoup



class Tag:
    def __init__(self, tag_name: str, text: str = '', attr: Dict[str, str] = None):
        self.tag_name = tag_name  # 元素的Tag名
        self.attr = attr if attr is not None else {}  # 元素的属性键值对
        self.text = text  # 元素的文本内容

    def parse(self, element):
        """根据 BeautifulSoup element 解析 Tag 对象"""
        self.tag_name = element.name
        self.text = element.get_text(strip=True)
        self.attr = element.attrs

    def build(self):
        """根据 Tag 对象构建 BeautifulSoup element"""
        tag = BeautifulSoup('', 'html.parser').new_tag(self.tag_name, attrs=self.attr)
        tag.string = self.text
        return tag

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text[:20]


class Head:
    def __init__(self):
        self.title = 'Untitled'  # 头部元素中的标题元素
        self.other_elem: List[Tag] = []  # 头部其他元素，例如 meta、link 等
        self.attr = {}  # 头部元素本身的属性

    def add_element(self, tag: Tag):
        self.other_elem.append(tag)

    def clone(self, title: str):
        new_head = Head()
        new_head.title = title
        new_head.attr = self.attr
        new_head.other_elem = self.other_elem.copy()
        return new_head

    def parse(self, element):
        """解析 head 元素"""
        self.title = element.find('title').get_text(strip=True) if element.find('title') else 'Untitled'
        self.other_elem = []
        for tag in element.find_all(True):  # 找出所有标签
            if tag.name != 'title':  # 排除 <title> 标签
                tag_obj = Tag(tag.name, tag.get_text(strip=True), tag.attrs)
                self.other_elem.append(tag_obj)

    def build(self):
        """根据 Head 对象构建 head 部分的 HTML"""
        head_tag = BeautifulSoup('', 'html.parser').new_tag('head', **self.attr)
        title_tag = BeautifulSoup('', 'html.parser').new_tag('title')
        title_tag.string = self.title
        head_tag.append(title_tag)
        for tag_obj in self.other_elem:
            head_tag.append(tag_obj.build())
        return head_tag


class Body:
    def __init__(self):
        self.attr = {}  # body元素本身的属性
        self._paras: List[Tag] = []  # 存储正文中的各个 Tag 元素（类型为 p、h1~h6、div 等）

    def add_paras(self, *tags: Tag):
        for tag in tags:
            self._paras.append(tag)

    def clone(self):
        new_body = Body()
        new_body.attr = self.attr
        return new_body

    def paragraphs(self):
        for index, tag in enumerate(self._paras):
            if tag.tag_name != 'div':
                yield index, tag

    def get_paras(self):
        return self._paras

    def set_para(self, para_list: List[Tag]):
        self._paras = para_list

    def parse(self, element):
        """解析 body 元素"""
        self.attr = element.attrs
        self._paras = []
        for tag in element.find_all(True):  # 找出所有标签
            tag_obj = Tag(tag.name, tag.get_text(strip=True), tag.attrs)
            self._paras.append(tag_obj)

    def build(self):
        """根据 Body 对象构建 body 部分的 HTML"""
        body_tag = BeautifulSoup('', 'html.parser').new_tag('body', **self.attr)
        for tag_obj in self._paras:
            body_tag.append(tag_obj.build())
        return body_tag

    def __getitem__(self, index):
        return self._paras[index]

    def __setitem__(self, index, value):
        if not isinstance(value, Tag):
            raise TypeError("Assigned value must be an instance of Tag")
        self._paras[index] = value

    def __delitem__(self, index):
        del self._paras[index]

    def __len__(self):
        return len(self._paras)

    def __iter__(self):
        return iter(self._paras)

    def __repr__(self):
        return f"Body({len(self._paras)} paragraphs)"

    def __add__(self, other):
        new_body = self.clone()
        if isinstance(other, self.__class__):
            new_body._paras = self._paras + other._paras
            return new_body
        else:
            raise TypeError


class Chapter:
    def __init__(self, path=None):
        self.path = None
        self.head = Head()
        self.body = Body()
        self.attr = {}  # HTML 元素的属性
        self.xml_note = "<?xml version='1.0' encoding='utf-8'?>"
        if path is not None:
            self.load_from_file(path)

    @property
    def title(self):
        return self.head.title

    def clone(self, title: str = "Untitled"):
        new_chapter = Chapter()
        new_chapter.head = self.head.clone(title)
        new_chapter.body = self.body.clone()
        new_chapter.attr = self.attr.copy()
        new_chapter.xml_note = self.xml_note
        return new_chapter

    def set_title(self, title: str):
        self.head.title = title
        return self

    def save_to_file(self, filename: str):
        """将 Chapter 对象保存到 HTML 文件"""
        html_tag = BeautifulSoup('', 'html.parser').new_tag('html', **self.attr)
        html_tag.append(self.head.build())
        html_tag.append(self.body.build())
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.xml_note)
            file.write(str(html_tag.prettify()))

    def load_from_file(self, filename: str):
        """从 HTML 文件加载数据到 Chapter 对象"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file {filename} does not exist.")
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        soup = BeautifulSoup(content, 'html.parser')
        self.attr = soup.attrs
        self.head.parse(soup.head)
        self.body.parse(soup.body)
        return self

    def is_empty(self):
        return len(self.body.get_paras()) == 0

    def __getitem__(self, index):
        return self.body[index]

    def __setitem__(self, index, value):
        self.body[index] = value

    def __delitem__(self, index):
        del self.body[index]

    def __len__(self):
        return len(self.body)

    def __repr__(self):
        return f"Chapter(Title: {self.head.title}, {len(self.body)} paragraphs)"


def is_volume(text: str):
    volume_regx = re.compile(r"^\s*第[零一二三四五六七八九十百千万0-9]卷")
    return bool(volume_regx.search(text)) and "完" not in text


def is_chapter(text: str):
    chapter_regx = re.compile(r"第[零一二三四五六七八九十百千万0-9]+章|楔子")
    return bool(chapter_regx.search(text)) and "完" not in text


def fit_space(input_string):
    return re.sub(r'\s+', ' ', input_string).strip()


