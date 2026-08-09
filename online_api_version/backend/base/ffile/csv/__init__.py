import csv


class Casv(list):
    """用于csv读取、存储和写入的类

    初始化时，适应给出的参数 来`构建实例`或者`输出到文件`
    - `get()` 用于主动从文件输入数据到实例
    - `put()` 用于向指定文件输入实例中的数据"""
    name: str
    title: list[str]
    item: list[list[str]]

    def __init__(self, *args, **kwargs):
        """创建一个CsvList类，三个参数：
        - `file` 文件名 (可不指名)
        - `title` 标题行 (一个n元列表)
        - `item` 数据行列表 (一个n元列表的列表)
        ### 文件名 -> 读取文件 | 数据 -> 生成实例 | 全部 -> 输出文件
        1. 当 `只给文件名` 时尝试打开文件读取到实例中（该情况下不用指明变量名）
        2. 当 `给了标题行和数据行列表` 时将其存储到实例中
        3. 当 `参数齐全` 时尝试输出到目标文件中
        """
        super().__init__()
        if args and isinstance(args[0], str):
            file = args[0]
        elif 'file' in kwargs:
            file = kwargs['file']
        else:
            file = 'example.csv'

        self.name = file

        if kwargs:
            if 'title' in kwargs and 'item' in kwargs:
                self.__build(kwargs['title'], kwargs['item'])
            else:
                raise KeyError(f'参数错误: {str(kwargs)}')
        else:
            try:
                self.get(file)
            except Exception as e:
                raise ValueError(f"初始化时尝试读取文件出错: {e}")

    def __build(self, title: list[str], item: list[list[str]]):
        self.title = title
        self.item = item
        self.put()

    # 从文件获取
    def get(self, file):
        """
        从指定的CSV文件读取数据并存储到实例中。
        
        参数:
        - file (str): 指定的CSV文件路径。
        
        """
        self.name = file
        try:
            with open(file, 'r') as file:
                li = list(csv.reader(file))
                if not li:
                    raise ValueError("文件内容为空")
                self.title = li[0]
                if li[1]:
                    self.item = li[1:]
                file.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"文件 {file} 未找到")
        except Exception as e:
            raise ValueError(f"读取文件时出错: {e}")

    # 输出到文件
    def put(self, file: str = ''):
        """
        将实例中的数据写入到指定的CSV文件中(默认 `self.name`)。
        
        参数:
        - `file (str)`: 目标CSV文件路径。如果未指定，默认使用 `self.name` 作为文件名。
        
        注意:
        - 该函数会先写入标题行，然后写入数据行。
        """
        if not hasattr(self, 'title') or not hasattr(self, 'item'):
            raise ValueError("实例没有 title 或 item 属性，无法写入")
        if not file:
            file = self.name
        with open(file, 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(self.title)
            for i in self.item:
                writer.writerow(i)

    # 取数组有关
    def __getitem__(self, index):
        """
        重载索引运算符，以便可以使用索引从实例中获取数据。
        
        参数:
        - index (int): 索引值。
        
        返回:
        - 返回对应的数据行。如果索引为0或负，则返回标题行。
        
        异常:
        - 如果索引超出数据的范围，会引发一个 IndexError 异常。
        """
        if index <= 0:
            return self.title
        if index > len(self.item):
            raise IndexError("索引超出范围")
        return self.item[index - 1]

    # 迭代器有关
    def __len__(self):
        return len(self.item)

    def __iter__(self):
        """
        返回一个迭代器对象，以便可以在for循环中迭代实例中的数据行。

        返回:
        - 返回迭代器对象（self）。
        """
        self.current = 0
        return self

    def __next__(self):
        """
        返回下一个数据行。用于支持迭代器协议。

        返回:
        - 返回下一个数据行。
        - 如果所有的数据行都已经被迭代完了，会引发一个 StopIteration 异常以使迭代正常结束
        """
        if self.current < len(self.item):
            self.current += 1
            return self.item[self.current - 1]
        else:
            raise StopIteration

    # 加法有关
    def __add__(self, other):
        """
        重载加法运算符，以便可以合并两个实例或将一个数据列表添加到实例中。
        
        参数:
        - `other (CCsv or list)`: 另一个CCsv实例或一个数据列表。
        
        返回:
        - 返回一个新的CCsv实例，其中包含合并后的数据。
        
        """
        if isinstance(other, Casv):
            return Casv(title=self.title, item=self.item + other.item)
        elif isinstance(other, list):
            if not other:
                raise ValueError("尝试添加的列表为空")
            if isinstance(other[0], str):
                li = self.item + [other]
                return Casv(title=self.title, item=li)
            elif isinstance(other[0], list):
                li = self.item + other
                return Casv(title=self.title, item=li)

    # 输出有关
    def __repr__(self):
        title = str(self.title)
        div = '\n' + len(title) * '-' + '\n'
        items = ''
        for i in self.item:
            items += str(i) + '\n'
        return title + div + items
