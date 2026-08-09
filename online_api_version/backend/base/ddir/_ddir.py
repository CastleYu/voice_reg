import fnmatch
import os

project_excludes = [
    # 一般版本控制系统文件夹
    ".git", ".svn", ".hg", ".bzr",

    # Python 项目
    "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.egg-info", "*.egg", "*.whl",

    # 虚拟环境
    "venv", ".env", ".venv", "env.bak", "venv.bak",

    "*.tmp", "*.bak", "*.swp", "*.swo", "*.DS_Store",

    # 文档和二进制输出
    "*.out", "*.o", "*.obj", "*.class", "*.war", "*.ear", "*.dylib",

    # 前端项目
    "node_modules", "bower_components",

    # 编译生成的中间文件
    "CMakeFiles", "CMakeCache.txt", "*.cmake", "Makefile", "*.so", "*.a", "*.lib",

    # IDE 配置文件和缓存
    ".idea", "*.iml", ".vscode", "*.code-workspace", ".classpath", ".project", ".settings/",

    # Jupyter Notebook 检查点
    ".ipynb_checkpoints",

    # 操作系统特定文件
    ".DS_Store", "Thumbs.db", ".AppleDouble", ".LSOverride", "__MACOSX",
]


class DiskPath:
    def __new__(cls, path=None):
        if path is None:
            path = os.getcwd()
        if isinstance(path, DiskPath):  # 如果传入的是 DiskPath 对象
            return path  # 直接返回原对象
        return super(DiskPath, cls).__new__(cls)  # 否则创建新对象

    def __init__(self, path=None):
        if path is None:
            path = os.getcwd()
        if isinstance(path, DiskPath):  # 如果是 DiskPath 对象，初始化已跳过
            return
        if len(path) == 2:
            if path[1] == ':':
                path = path + os.path.sep
        self._path = os.path.normpath(path)

    @property
    def abs_path(self):
        """获取绝对路径"""
        return os.path.abspath(self._path)

    @property
    def rel_path(self):
        """获取相对路径，每次访问时基于当前工作目录更新"""
        return os.path.relpath(self.abs_path, os.getcwd())

    @property
    def folder(self):
        return os.path.dirname(self.abs_path)

    @property
    def dir_name(self):
        """获取目录名"""
        return os.path.dirname(self.abs_path)

    @property
    def drive(self):
        """获取路径盘符"""
        return os.path.splitdrive(self.abs_path)[0]

    @property
    def basename_with_ext(self):
        """获取包含扩展名的文件名"""
        return os.path.basename(self.abs_path)

    @property
    def basename_no_ext(self):
        """获取不带扩展名的文件名"""
        if self.is_dir:
            return os.path.basename(self.abs_path)
        return os.path.splitext(self.basename_with_ext)[0]

    @property
    def name(self):
        return self.basename_no_ext

    @property
    def ext(self):
        """获取文件扩展名"""
        return os.path.splitext(self.basename_with_ext)[1]

    @property
    def ext_only(self):
        return os.path.splitext(self.basename_with_ext)[1].strip('.')

    @property
    def exists(self):
        """检查路径是否存在"""
        return os.path.exists(self.abs_path)

    @property
    def is_file(self):
        """检查路径是否为文件"""
        return os.path.isfile(self.abs_path)

    @property
    def is_dir(self):
        """检查路径是否为文件夹"""
        return os.path.isdir(self.abs_path)

    @property
    def has_valid_driver(self):
        return os.path.exists(self.drive)

    @property
    def is_driver(self):
        """检查路径是否是挂载点 (Win的盘符，Linux的/)"""
        return os.path.ismount(self.abs_path)

    @property
    def time(self):
        """获取文件修改时间戳 (默认的修改时间戳) """
        if not self.exists:
            return 0
        return os.path.getmtime(self.abs_path)

    @property
    def size(self):
        """获取文件或文件夹的大小 (字节 Bytes)"""
        if not self.exists:
            return 0
        if os.path.isfile(self.abs_path):
            return os.path.getsize(self.abs_path)
        elif os.path.isdir(self.abs_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(self.abs_path):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
            return total_size
        else:
            raise ValueError(f"路径无效：{self.abs_path}")

    @property
    def size_str(self):
        units = ["B", "KB", "MB", "GB", "TB"]
        size_in_bytes = self.size
        unit_index = 0

        # 持续除以 1024，直到找到合适的单位
        while size_in_bytes >= 1024 and unit_index < len(units) - 1:
            size_in_bytes /= 1024
            unit_index += 1

        return f"{size_in_bytes:.2f} {units[unit_index]}"

    def join(self, *paths):
        """拼接路径并更新路径"""
        if self.is_file:
            raise NotADirectoryError(f"[Not a Folder] Path {self.abs_path} is not a folder(directory)")
        self._path = os.path.join(self._path, *paths)
        return self

    def follow(self, folder):
        """重新作为子文件夹拼接到指定路径"""
        self._path = os.path.join(folder, self.basename_with_ext)
        return self

    def leave(self):
        """退出到当前的父文件夹"""
        self._path = os.path.dirname(self.abs_path)
        return self

    def cd(self, folder):
        tgt_path = os.path.join(self.abs_path, folder)
        if not self.exists or (self.is_dir and os.path.isdir(tgt_path)):
            self._path = tgt_path
        else:
            print("Chdir Failed")
        return self

    def need_file(self, new_path):
        """确保指定的路径是一个文件，并且路径所指向的文件是有效的。"""
        if not self.exists or self.is_dir:
            new_dp = DiskPath(new_path)
            if new_dp.is_file:
                return new_dp
            else:
                raise IsADirectoryError(f"[Not a File] Path {new_path} is not a file")
        elif self.has_valid_driver:
            return self
        else:
            raise ValueError(f"[Invalid Driver] Path {new_path} is not in a accessible driver")

    def need_dir(self, new_path):
        """确保指定的路径是一个目录，并且路径所指向的目录是有效的"""
        if not self.exists or self.is_file:
            new_dp = DiskPath(new_path)
            if new_dp.is_dir:
                return new_dp
            else:
                raise NotADirectoryError(f"[Not a Folder] Path {new_path} is not a folder")
        elif self.has_valid_driver:
            return self
        else:
            raise ValueError(f"[Invalid Driver] Path {new_path} is not in a accessible driver")

    @property
    def fill_user_path(self):
        return os.path.expanduser(self._path)

    def apply_user_path(self):
        """基于 expanduser() 处理用户路径"""
        self._path = self.fill_user_path
        return self

    @property
    def fill_env_var(self):
        return os.path.expandvars(self._path)

    def apply_env_var(self):
        """基于 expandvars() 处理环境变量"""
        self._path = self.fill_env_var
        return self

    def assure(self, need_file=False):
        """确保路径存在，如果是文件夹路径则创建文件夹"""
        if not self.exists:
            if self.is_dir or self._path.endswith(os.sep):
                os.makedirs(self.abs_path, exist_ok=True)
            elif self.is_file:
                dir_name = os.path.dirname(self.abs_path)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                with open(self.abs_path, 'w', encoding='utf8') as f:
                    pass
            else:
                if need_file:
                    with open(self.abs_path, 'w', encoding='utf8') as f:
                        pass
                else:
                    os.makedirs(self.abs_path, exist_ok=True)
        return self

    def __eq__(self, other):
        """基于 samefile() 实现 == 操作"""
        if isinstance(other, DiskPath):
            if self.exists:
                return os.path.samefile(self.abs_path, other.abs_path)
            else:
                return False
        elif isinstance(other, str):
            other = DiskPath(other)
            if self.exists:
                return os.path.samefile(self.abs_path, other.abs_path)
            else:
                return False
        return NotImplemented

    def equal(self, other):
        """基于 samestat() 实现 equal() 方法"""
        if isinstance(other, DiskPath):
            try:
                return os.path.samestat(os.stat(self.abs_path), os.stat(other.abs_path))
            except FileNotFoundError:
                return False
        return NotImplemented

    def __and__(self, other):
        """基于 commonpath() 实现 & 运算"""
        if isinstance(other, DiskPath):
            common_path = os.path.commonpath([self.abs_path, other.abs_path])
            return DiskPath(common_path)
        else:
            common_path = os.path.commonpath([self.abs_path, other])
            return DiskPath(common_path)

    def __str__(self):
        return self.abs_path

    def __repr__(self):
        return self.abs_path

    def __fspath__(self):
        """让 FilePath 被视作 PathLike"""
        return self.abs_path

    def __add__(self, other):
        if self.is_file:
            raise NotADirectoryError(f"[Not a Folder] Path {self.abs_path} is not a folder(directory)")
        if isinstance(other, DiskPath):
            return DiskPath(os.path.join(self._path, other._path))
        else:
            return DiskPath(os.path.join(self._path, other))

    def __getitem__(self, index):
        """支持索引操作"""
        return self.deepening_path()[index]

    def __contains__(self, item):
        """支持 in 操作"""
        return item in self.deepening_path()

    def __iter__(self):
        for i in os.listdir(self.abs_path):
            yield os.path.join(self.abs_path, i)

    def deepening_path(self):
        path = self._path
        parts = []
        while True:
            path, tail = os.path.split(path)
            if tail:
                parts.insert(0, tail)
            else:
                if path:  # 添加根路径
                    parts.insert(0, path)
                break
        return parts

    def list(self, including_folder=True):
        """获取当前目录的所有文件（不递归）"""
        if self.is_file:
            raise NotADirectoryError(f"[Not a Folder] Path {self.abs_path} is not a folder(directory)")
        return [
            DiskPath(os.path.join(self.abs_path, f))
            for f in os.listdir(self.abs_path)
            if os.path.isfile(os.path.join(self.abs_path, f)) or (
                    including_folder and os.path.isdir(os.path.join(self.abs_path, f)))
        ]

    def list_recurse(self, including_folder=False):
        """递归获取目录下的所有文件"""
        if self.is_file:
            raise NotADirectoryError(f"[Not a Folder] Path {self.abs_path} is not a folder(directory)")
        items = []
        for root, dirs, files in os.walk(self.abs_path):
            if including_folder:
                # 将子文件夹添加到结果
                items.extend(DiskPath(os.path.join(root, d)) for d in dirs)
            # 将文件添加到结果
            items.extend(DiskPath(os.path.join(root, f)) for f in files)
        return items

    def filter(self, include: list = None, exclude: list = None, including_folder: bool = True):
        """按条件筛选当前目录的文件和文件夹（不递归）"""
        if include is None:
            include = ['*']
        if exclude is None:
            exclude = project_excludes
        if not self.is_dir:
            raise NotADirectoryError(f"{self.abs_path} is not a directory.")
        for item in os.listdir(self.abs_path):
            item_path = os.path.join(self.abs_path, item)
            dp = DiskPath(item_path)
            if os.path.isfile(item_path) or (including_folder and os.path.isdir(item_path)):
                if any(fnmatch.fnmatch(item, pattern) for pattern in include) and not any(
                        fnmatch.fnmatch(item, pattern) for pattern in exclude
                ):
                    yield dp

    def filter_recurse(self, include: list = None, exclude: list = None, including_folder: bool = False):
        """按条件递归筛选文件和文件夹"""
        if include is None:
            include = ['*']
        elif not isinstance(include, list):
            include = [include]
        if exclude is None:
            exclude = project_excludes
        elif not isinstance(exclude, list):
            exclude = [exclude]
        if not self.is_dir:
            raise NotADirectoryError(f"{self.abs_path} is not a directory.")
        for root, dirs, files in os.walk(self.abs_path):
            if including_folder:
                for folder in dirs:
                    folder_path = os.path.join(root, folder)
                    if any(fnmatch.fnmatch(folder, pattern) for pattern in include) and not any(
                            fnmatch.fnmatch(folder, pattern) for pattern in exclude
                    ):
                        yield DiskPath(folder_path)
            for file in files:
                file_path = os.path.join(root, file)
                if any(fnmatch.fnmatch(file, pattern) for pattern in include) and not any(
                        fnmatch.fnmatch(file, pattern) for pattern in exclude
                ):
                    yield DiskPath(file_path)


# noinspection PyUnresolvedReferences
os.PathLike.register(DiskPath)
if __name__ == '__main__':
    dp = DiskPath(__file__)
    dp = DiskPath(dp.dir_name)
    print(DiskPath(dp))
    print("dp.abs_path= ", dp.abs_path)  # abs 绝对路径
    print("dp.rel_path= ", dp.rel_path)  # r 当前的相对路径
    print("dp.dir_name= ", dp.dir_name)  # dn 父目录名
    print("dp.drive= ", dp.drive)  # dr 盘符
    print("dp.basename_with_ext= ", dp.basename_with_ext)  # bwe
    print("dp.basename_no_ext= ", dp.basename_no_ext)  # bne
    print("dp.name= ", dp.name)
    print("dp.ext= ", dp.ext)
    print("dp.exists= ", dp.exists)
    print("dp.is_file= ", dp.is_file)
    print("dp.is_dir= ", dp.is_dir)
    print("dp.is_driver= ", dp.is_driver)
    print("dp.time= ", dp.time)
    print("dp.size= ", dp.size)
    print("dp.size_str= ", dp.size_str)
    print("dp.fill_user_path= ", dp.fill_user_path)
    print("dp.fill_env_var= ", dp.fill_env_var)

    print("dp.join('base')= ", dp.join('base'))
    print("dp.follow= ", dp.follow("base"))
    print("dp.leave()= ", dp.leave())
    print("dp.cd('base')= ", dp.cd('base'))
    print("dp.apply_user_path()= ", dp.apply_user_path())
    print("dp.apply_env_var()= ", dp.apply_env_var())
    print("dp.assure()= ", dp.assure())
    dp2 = DiskPath(dp.abs_path)
    print("dp == dp2= ", dp == dp2)
    print("dp.equal(dp2)= ", dp.equal(dp2))
    print("dp & dp2.leave()= ", dp & dp2.leave())
    print("str(dp)= ", str(dp))
    print("[dp, dp]= ", [dp, dp])
    print("dp + 'ggodd'= ", dp + 'ggodd')
    dp3 = DiskPath('base')
    print("dp + dp3= ", dp + dp3)
    print("dp[2]= ", dp[2])
    print("'casyuGallery' in dp= ", 'casyuGallery' in dp)
    for i in dp:
        print("i= ", i)
    print("dp.deepening_path()= ", dp.deepening_path())
    print("dp.list()= ", dp.list())
    print("dp.list_recurse()= ", dp.list_recurse())
    print("dp.filter()= ", dp.filter())
    print("dp.filter_recurse()= ", dp.filter_recurse())
