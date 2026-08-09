import ctypes
import hashlib
import logging
import os
import subprocess
import time
from ctypes import wintypes
from io import BytesIO

import win32com.client
from PIL import Image

Image._plugins = [
    "BmpImagePlugin",
    "IcoImagePlugin",
    "JpegImagePlugin",
    "Jpeg2KImagePlugin",
    "MpegImagePlugin",
    "PdfImagePlugin",
    "PngImagePlugin",
    "PsdImagePlugin",
    "TiffImagePlugin",
    "WebPImagePlugin"
]
Image.init()

# 定义常量
FCS_FORCEWRITE = 0x00000002  # 强制写入设置
FCSM_ICONFILE = 0x00000010  # 用于设置图标文件


class GUID(ctypes.Structure):
    """
    GUID 结构体，用于表示全局唯一标识符。

    字段：
        Data1: DWORD 类型的标识符数据1。
        Data2: WORD 类型的标识符数据2。
        Data3: WORD 类型的标识符数据3。
        Data4: BYTE 数组类型的标识符数据4。
    """
    # noinspection PyTypeChecker
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]


class SHFOLDERCUSTOMSETTINGS(ctypes.Structure):
    """
    SHFOLDERCUSTOMSETTINGS 结构体，用于定义文件夹自定义设置。

    字段：
        dwSize: 结构体大小，单位为字节。
        dwMask: 属性掩码，定义要更改的设置类型。
        pvid: SHELLVIEWID 指针，用于指定视图 ID。
        pszWebViewTemplate: WebView 模板路径。
        cchWebViewTemplate: WebView 模板路径长度。
        pszWebViewTemplateVersion: WebView 模板版本。
        pszInfoTip: 文件夹信息提示文本。
        cchInfoTip: 信息提示文本长度。
        pclsid: CLSID 指针，用于指定类 ID。
        dwFlags: 其他标志位。
        pszIconFile: 图标文件路径。
        cchIconFile: 图标文件路径长度。
        iIconIndex: 图标索引。
        pszLogo: 文件夹徽标路径。
        cchLogo: 徽标路径长度。
    """
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("dwMask", wintypes.DWORD),
        ("pvid", ctypes.POINTER(GUID)),
        ("pszWebViewTemplate", wintypes.LPWSTR),
        ("cchWebViewTemplate", wintypes.DWORD),
        ("pszWebViewTemplateVersion", wintypes.LPWSTR),
        ("pszInfoTip", wintypes.LPWSTR),
        ("cchInfoTip", wintypes.DWORD),
        ("pclsid", ctypes.POINTER(GUID)),
        ("dwFlags", wintypes.DWORD),
        ("pszIconFile", wintypes.LPWSTR),
        ("cchIconFile", wintypes.DWORD),
        ("iIconIndex", ctypes.c_int),
        ("pszLogo", wintypes.LPWSTR),
        ("cchLogo", wintypes.DWORD),
    ]


class IconSetter:
    def __init__(self, icon_path, icon_index: int = 0):
        self.fcs = SHFOLDERCUSTOMSETTINGS()
        self.fcs.dwSize = ctypes.sizeof(SHFOLDERCUSTOMSETTINGS)
        self.fcs.dwMask = FCSM_ICONFILE
        self.fcs.pvid = None
        self.fcs.pszWebViewTemplate = None
        self.fcs.cchWebViewTemplate = 0
        self.fcs.pszWebViewTemplateVersion = None
        self.fcs.pszInfoTip = None
        self.fcs.cchInfoTip = 0
        self.fcs.pclsid = None
        self.fcs.dwFlags = 0
        self.fcs.cchIconFile = 0
        self.fcs.pszLogo = None
        self.fcs.cchLogo = 0
        self.load_icon(icon_path, icon_index)

    def load_icon(self, icon_path, icon_index: int = 0):
        self.fcs.pszIconFile = icon_path
        self.fcs.iIconIndex = icon_index
        return self

    def set_folder(self, folder_path: str):
        """
        设置文件夹的自定义图标。

        参数：
            folder_path (str): 文件夹路径。
            icon_path (str): 图标文件路径。
            icon_index (int): 图标索引，默认为 0。

        说明：
            调用 Windows API 的 SHGetSetFolderCustomSettings 函数，
            设置文件夹的自定义图标。
        """

        shell32 = ctypes.windll.shell32
        # 调用 SHGetSetFolderCustomSettings
        result = shell32.SHGetSetFolderCustomSettings(
            ctypes.byref(self.fcs),
            folder_path,
            FCS_FORCEWRITE
        )

        if result != 0:  # 如果返回值不是 S_OK
            error_message = f"Failed: Set {folder_path}. Error code: {result}"
            raise ctypes.WinError(result, error_message)

    def set_lnk(self, shortcut_path):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.IconLocation = str(self.fcs.pszIconFile)
        shortcut.Save()


class IconMaker:
    def __init__(self, image_path, side_length=256):
        self.image_path = image_path
        self.load_image(image_path)
        self.side_length = side_length
        self.build_board()

    def load_image(self, image_path):
        """加载图像"""
        self.img = Image.open(image_path)
        self.img_width, self.img_height = self.img.size
        return self

    def build_board(self):
        """创建一个透明的背景图像，大小为正方形"""
        self.square_size = max(self.img_width, self.img_height)
        self.board = Image.new("RGBA", (self.square_size, self.square_size), (0, 0, 0, 0))
        self.processed = False
        return self

    def put_img(self, box=None):
        """将原图粘贴到新图像的中心"""
        if box is None:
            box = (self.square_size - self.img_width) // 2, (self.square_size - self.img_height) // 2
        self.board.paste(self.img, box)
        self.board = self.board.resize((self.side_length, self.side_length), Image.Resampling.LANCZOS)
        self.processed = True
        return self

    def generate_md5_hash(self, image):
        """计算图像的MD5哈希值"""
        # 将图像保存到内存中的字节流
        with BytesIO() as byte_io:
            image.save(byte_io, format='PNG')  # 保存为PNG格式
            img_data = byte_io.getvalue()
        # 计算MD5哈希值
        md5_hash = hashlib.md5(img_data).hexdigest()
        return md5_hash

    def save_icon(self, output_dir=None):
        """保存图像到文件夹"""
        # 获取MD5哈希值
        if output_dir is None:
            output_dir = os.path.dirname(self.image_path)
            logging.warning(f"保存到原有的目录：{output_dir}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        board_hash = self.generate_md5_hash(self.board)
        # 保存图标到文件夹
        output_path = os.path.join(output_dir, f'{board_hash}.ico')
        self.board.save(output_path, format="ICO")

        return output_path

    def make(self, output_dir=None, box=None):
        """全流程方法：加载图像、处理图像、生成图标并保存"""
        self.load_image(self.image_path)
        self.build_board()
        self.put_img(box)
        return self.save_icon(output_dir)


class IconFixer:
    @staticmethod
    def _close_explorer():
        """终止资源管理器进程"""
        subprocess.call('taskkill /f /im explorer.exe', shell=True)
        time.sleep(2)  # 等待几秒，确保资源管理器已关闭

    @staticmethod
    def _delete_cache():
        """删除图标缓存"""
        icon_cache_path = os.path.join(
            os.getenv('LOCALAPPDATA'), 'Microsoft', 'Windows', 'Explorer')

        if os.path.exists(icon_cache_path):
            for file in os.listdir(icon_cache_path):
                if file.startswith('iconcache') or file.startswith('thumbcache'):
                    try:
                        os.remove(os.path.join(icon_cache_path, file))
                        print(f"删除缓存文件: {file}")
                    except Exception as e:
                        print(f"删除缓存文件失败: {e}")

    @staticmethod
    def _restart_explorer():
        """重新启动资源管理器进程"""
        subprocess.call('start explorer.exe', shell=True)
        time.sleep(2)  # 等待资源管理器重新启动

    @staticmethod
    def _refresh_folder_icon(folder_path):
        """使用 Shell API 刷新文件夹图标"""
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.Namespace(folder_path)
        try:
            folder.Items().Item(0).InvokeVerb("refresh")  # 触发刷新命令
            print(f"刷新文件夹图标: {folder_path}")
        except Exception as e:
            print(f"刷新文件夹图标失败: {e}")

    @staticmethod
    def hard_reCache(folder_path):
        print("关闭资源管理器...")
        IconFixer._close_explorer()

        print("删除图标缓存...")
        IconFixer._delete_cache()

        print("重启资源管理器...")
        IconFixer._restart_explorer()

        print("刷新文件夹图标...")
        IconFixer._refresh_folder_icon(folder_path)

    @staticmethod
    def soft_refresh(folder_path):
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.Namespace(folder_path)
        folder.Items().Item(0).InvokeVerb("refresh")  # 触发刷新命令
