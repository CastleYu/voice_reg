import ctypes
import os.path
import tkinter as tk
from tkinter import filedialog

default_filetypes = [
    ("任意类型", "*.*"),
    ("文本文件", "*.txt"),
    ("Python", "*.py"),
    ("JSON", "*.json"),
    ("Csv文件", "*.csv"),
    ("图像", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
    ("音频", "*.mp3;*.wav;*.aac;*.flac"),
    ("视频", "*.mp4;*.mkv;*.avi;*.mov;*.wmv"),
    ("文档", "*.pdf;*.doc;*.docx;*.ppt;*.pptx;*.xls;*.xlsx"),
    ("压缩文件", "*.zip;*.rar;*.7z;*.tar;*.gz"),
]


def set_dpi_awareness(debug=False):
    try:
        if debug:
            print('尝试设置自适应DPI……')
        # 尝试设置应用程序的DPI感知，以便在高DPI屏幕上正确缩放
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        if debug:
            print('设置自适应DPI成功')
    except Exception as e:
        print(f"设置自适应DPI失败 {e}")
        # DPI感知设置失败可能是因为缺少权限，或该API在当前Windows版本中不可用


def ask_directory():
    # 设置DPI自适应
    set_dpi_awareness()

    # 创建一个Tkinter根窗口，但不显示它
    root = tk.Tk()
    root.withdraw()

    # 打开目录选择对话框并获取选择的目录
    directory_path = filedialog.askdirectory()

    # 检查用户是否选择了目录，且保证目录存在
    if directory_path:
        directory_path = os.path.join(
            *os.path.split(os.path.abspath(directory_path)))
        print(f"选择目录： {directory_path}")
    else:
        raise FileExistsError('未选择路径或路径不存在')
    # 销毁根窗口
    root.destroy()
    return directory_path


def ask_file(filetypes=None):
    if filetypes is None:
        filetypes = default_filetypes
    set_dpi_awareness()

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=filetypes)

    if file_path:
        file_path = os.path.abspath(file_path)
        print(f"选择文件： {file_path}")
    else:
        raise FileExistsError('未选择文件或文件不存在')
    root.destroy()
    return file_path


def ask_file_list(filetypes=None):
    if filetypes is None:
        filetypes = default_filetypes
    set_dpi_awareness()

    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(filetypes=filetypes)

    if file_paths:
        file_paths = [os.path.abspath(file_path) for file_path in file_paths]
        print(f"选择的文件列表： {file_paths}")
    else:
        raise FileExistsError('未选择文件或文件不存在')
    root.destroy()
    return file_paths


def ask_pdf():
    return ask_file(filetypes=[('pdf', '.pdf')])
