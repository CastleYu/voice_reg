import os
from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER

key = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
Downloads, _ = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')
Pictures, _ = QueryValueEx(key, 'My Pictures')
Desktop, _ = QueryValueEx(key, 'Desktop')
Music, _ = QueryValueEx(key, 'My Music')
Start_Menu, _ = QueryValueEx(key, 'Start Menu')
Documents, _ = QueryValueEx(key, 'Personal')


def init():
    global Downloads, Pictures, Desktop, Music, Start_Menu, Documents, key
    key = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    Downloads, _ = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')
    Pictures, _ = QueryValueEx(key, 'My Pictures')
    Desktop, _ = QueryValueEx(key, 'Desktop')
    Music, _ = QueryValueEx(key, 'My Music')
    Start_Menu, _ = QueryValueEx(key, 'Start Menu')
    Documents, _ = QueryValueEx(key, 'Personal')


# Downloads=Download
# Pictures=Picture
# Documents=Document


class DirectoryHelper:

    @staticmethod
    def get_current_script_name():
        """获取当前执行的脚本名称"""
        return os.path.basename(__file__)

    @staticmethod
    def list_current_directory_contents():
        """列出当前目录的内容，不包括子目录和当前执行的脚本"""
        filesAndFolders = os.listdir()
        currentScriptName = DirectoryHelper.get_current_script_name()

        # 确保列表中不包含此脚本的文件名
        if currentScriptName in filesAndFolders:
            filesAndFolders.remove(currentScriptName)

        return filesAndFolders

    @staticmethod
    def display_directory_contents(to_file=False, output_file_name='dirList.txt'):
        """显示当前目录的内容，可选择输出到指定的文件"""
        contents = DirectoryHelper.list_current_directory_contents()

        # 如果选择输出到文件
        if to_file:
            with open(output_file_name, 'w', encoding='utf-8') as outputFile:
                for item in contents:
                    outputFile.write(item + '\n')
        # 如果选择控制台输出
        else:
            for item in contents:
                print(item)


if __name__ == "__main__":
    # 输出到控制台
    DirectoryHelper.display_directory_contents()

    # 输出到文件
    DirectoryHelper.display_directory_contents(to_file=True)
