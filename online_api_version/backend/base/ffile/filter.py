import os
import ctypes
import tkinter as tk
from tkinter import filedialog
import sys
import questionary

from ds_ex.tipe import ensure, unpack_collection
from wrappers.try_or import tryorprint


def set_dpi_awareness():
    """
    设置自适应DPI，以确保在高DPI屏幕上正确缩放
    """
    try:
        print('尝试设置自适应DPI……')
        # 尝试设置应用程序的DPI感知
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        print('设置自适应DPI成功')
    except Exception as e:
        print(f"设置自适应DPI失败 {e}")


def choose_option(*options, msg="请选择一个选项：", default=None, cancel_option="取消"):
    # 解包传入的选项
    options = unpack_collection(options)

    # 添加取消选项
    if cancel_option and cancel_option not in options:
        options = list(options) + [cancel_option]

    # 支持交互式选择
    if sys.stdout.isatty():
        # 添加默认值显示在消息中
        if default and default in options:
            msg = f"{msg} (默认: {default})"

        # 使用 questionary 提供选择
        choice = questionary.select(
            msg,
            choices=options,
            default=default
        ).ask()

    # 非交互式选择模式，使用数字选择
    else:
        print(f"{msg}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        if default:
            print(f"(默认: {default})")

        while True:
            try:
                user_input = input("请输入选项的数字编号：")

                # 如果输入为空且存在默认值，直接返回默认值
                if not user_input and default:
                    choice = default
                    break

                user_input = int(user_input)
                if 1 <= user_input <= len(options):
                    choice = options[user_input - 1]
                    break
                else:
                    print(f"请输入 1 到 {len(options)} 之间的数字。")
            except ValueError:
                print("无效输入，请输入一个数字。")

    # 处理取消选项
    if choice == cancel_option:
        print("已取消选择。")
        return None

    if choice:
        print(f"你选择了: {choice}")
        return choice
    else:
        print("没有选择任何选项！")
        return None


class BatchFileProcessor:
    def __init__(self, file_extension=None, directory_path=None):
        """
        初始化BatchFileProcessor类
        :param file_extension: 要处理的文件类型（例如 '.txt' 或 '.jpg'）
        """
        self.directory_path = None
        if directory_path is None:
            self.ask_directory()
        else:
            self.directory_path = os.path.abspath(directory_path)

        # 如果未指定文件扩展名，先获取目录中的所有扩展名
        if file_extension is None:
            self.file_extension = self.ask_for_file_extension()
        else:
            self.file_extension = ensure(file_extension, file_extension.startswith('.'), lambda x: "." + file_extension)
        self.process_func = None

    def ask_directory(self):
        """
        打开目录选择对话框，让用户选择一个目录
        """
        # 设置DPI感知
        set_dpi_awareness()

        # 创建Tkinter根窗口，但不显示它
        root = tk.Tk()
        root.withdraw()

        # 打开目录选择对话框并获取选择的目录
        directory_path = filedialog.askdirectory()

        # 检查用户是否选择了目录
        if directory_path:
            self.directory_path = os.path.abspath(directory_path)
            print(f"选择目录： {self.directory_path}")
        else:
            raise FileExistsError('未选择路径或路径不存在')

        # 销毁根窗口
        root.destroy()

    def ask_for_file_extension(self):
        """
        遍历目录，获取所有文件扩展名，并让用户选择一个
        """
        extensions = set()
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext:
                    extensions.add(ext)

        if not extensions:
            raise ValueError("该目录中没有找到任何文件。")

        # 使用 choose_option 让用户选择扩展名
        return choose_option(*sorted(extensions), msg="请选择要处理的文件类型：")

    def process_files(self):
        """
        批量处理文件夹下的指定类型文件
        """
        if not self.directory_path:
            raise ValueError("未选择目录，请先调用 ask_directory 方法")

        # 遍历目录，筛选指定类型文件
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                if file.lower().endswith(self.file_extension):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)

    def process_file(self, file_path):
        """
        处理单个文件的方法，可以根据需要进行重写
        :param file_path: 文件的完整路径
        """
        # 示例处理逻辑：这里只是打印文件路径
        if self.process_func is not None:
            return self.process_func(file_path)
        print(f"处理文件： {file_path}")
        return None


# 使用示例
if __name__ == "__main__":
    # 创建一个批量处理文件的实例
    processor = BatchFileProcessor()  # 未指定文件类型，会提示选择
    try:
        processor.process_files()
    except Exception as e:
        print(f"发生错误：{e}")
