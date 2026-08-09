import os

import win32com

import win32com.client


class LnkBuilder:
    def __init__(self):
        self._target = None  # 快捷方式目标文件
        self._shortcut_name = None  # 快捷方式的名称
        self._working_dir = None  # 工作目录
        self._icon_location = None  # 图标位置
        self._arguments = None  # 启动参数

    def set_target(self, target):
        """设置快捷方式的目标路径"""
        self._target = target
        return self

    def set_shortcut_name(self, shortcut_name):
        """设置快捷方式名称"""
        self._shortcut_name = shortcut_name
        return self

    def set_working_dir(self, working_dir):
        """设置工作目录"""
        self._working_dir = working_dir
        return self

    def set_icon_location(self, icon_location):
        """设置快捷方式的图标路径"""
        self._icon_location = icon_location
        return self

    def set_arguments(self, arguments):
        """设置快捷方式的启动参数"""
        self._arguments = arguments
        return self

    def build(self, shortcut_folder):
        """创建快捷方式"""
        if not all([self._target, self._shortcut_name]):
            raise ValueError("目标文件和快捷方式名称不能为空")

        # 创建快捷方式文件名
        shortcut_path = os.path.join(shortcut_folder, f"{self._shortcut_name}.lnk")

        # 使用win32com创建快捷方式
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)

        # 设置快捷方式属性
        shortcut.TargetPath = self._target
        shortcut.WorkingDirectory = self._working_dir if self._working_dir else os.path.dirname(self._target)
        shortcut.IconLocation = self._icon_location if self._icon_location else self._target
        shortcut.Arguments = self._arguments if self._arguments else ""
        shortcut.Save()

        print(f"快捷方式已创建：{shortcut_path}")
        return shortcut_path
