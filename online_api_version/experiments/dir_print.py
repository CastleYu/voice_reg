import os

def print_directory_tree(root_dir, prefix=''):
    """
    递归打印目录结构。

    :param root_dir: 要遍历的根目录路径
    :param prefix: 用于树状显示的前缀
    """
    # 获取目录下的所有条目，按名称排序
    entries = sorted(os.listdir(root_dir))
    entries_count = len(entries)

    for index, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        is_last = index == (entries_count - 1)
        connector = '└── ' if is_last else '├── '
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_directory_tree(path, prefix + extension)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='打印指定目录的树状结构。')
    parser.add_argument('directory', nargs='?', default='.', help='要遍历的目录路径（默认是当前目录）')
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    print(root_dir)
    print_directory_tree(root_dir)

if __name__ == '__main__':
    main()
