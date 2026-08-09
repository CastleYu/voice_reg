import os
import fnmatch
import csv
import random
from math import ceil
from typing import Dict, List, Tuple
from collections import defaultdict

# def get_files_with_prefix_count(directory: str) -> dict:
#     files_by_prefix = defaultdict(list)

#     try:
#         with os.scandir(directory) as entries:
#             for entry in entries:
#                 if entry.is_file() and fnmatch.fnmatch(entry.name, '*_*.wav'):
#                     prefix = entry.name.split('_')[0]
#                     files_by_prefix[prefix].append(entry.path)

#     except FileNotFoundError:
#         print(f"The specified directory '{directory}' was not found.")
#         return {}
#     except PermissionError:
#         print(f"Permission denied when accessing the directory '{directory}'.")
#         return {}
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return {}

#     return files_by_prefix

def get_files_by_parent_folder(directory: str) -> dict:
    """
    递归遍历目录结构，收集最底层文件夹中的WAV文件

    参数:
        directory (str): 要遍历的根目录路径

    返回:
        dict: 键为最底层文件夹名称，值为该文件夹内所有WAV文件路径列表
    """
    file_groups = defaultdict(list)

    try:
        # 使用os.walk遍历所有子目录
        for root, dirs, files in os.walk(directory):
            # 如果当前目录没有子目录，说明是最底层目录
            if not dirs:
                # 获取当前目录名称
                folder_name = os.path.basename(root)
                # 筛选WAV文件
                wav_files = [
                    os.path.join(root, f)
                    for f in files
                    if fnmatch.fnmatch(f.lower(), '*.wav')
                ]
                # 如果有WAV文件则添加到字典
                if wav_files:
                    file_groups[folder_name].extend(wav_files)

    except FileNotFoundError:
        print(f"目录不存在: {directory}")
        return {}
    except PermissionError:
        print(f"无权访问目录: {directory}")
        return {}
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return {}

    return dict(file_groups)

def generate_test_and_train_info(files_by_prefix: Dict[str, List[str]]) -> Tuple[List[dict], List[dict]]:
    """
    改进版数据划分函数，支持以下特性：
    1. 动态调整划分比例
    2. 智能处理奇数文件数
    3. 增强数据验证
    4. 唯一性检查
    """
    test_info = []
    train_info = []
    username_counter = 1  # 用户名生成器

    # 有效性检查
    if not isinstance(files_by_prefix, dict):
        raise ValueError("输入参数必须是字典类型")

    for prefix, files in files_by_prefix.items():
        # 数据验证
        if not isinstance(files, list) or len(files) == 0:
            print(f"⚠️ 无效文件列表: {prefix}")
            continue

        # 去重处理
        unique_files = list(set(files))
        file_count = len(unique_files)

        # 最小数量检查（可配置）
        min_required = 2
        if file_count < min_required:
            print(f"⏩ 跳过 {prefix}，文件数不足 {min_required} 个（实际 {file_count}）")
            continue

        # 智能划分比例（可根据需求调整）
        train_ratio = 0.5  # 50% 训练数据
        test_ratio = 1 - train_ratio

        # 计算分割点（向上取整保证最少1个测试文件）
        split_index = ceil(file_count * train_ratio)

        # 打乱顺序（保持可复现性）
        shuffled = random.sample(unique_files, file_count)

        # 划分数据集
        train_files = shuffled[:split_index]
        test_files = shuffled[split_index:]

        # 用户信息生成
        username = f"Test{username_counter}"
        permission_level = random.randint(1, 7)
        username_counter += 1  # 确保唯一性

        # 构建训练记录
        train_info.extend([
            {
                'filename': f,
                'username': username,
                'permission_level': permission_level
            } for f in train_files
        ])

        # 构建测试记录
        test_info.extend([
            {
                'filename': f
            } for f in test_files
        ])

        # 打印调试信息
        print(f"✅ 处理完成 {prefix}:")
        print(f"  训练文件: {len(train_files)} 个 | 测试文件: {len(test_files)} 个")
        print(f"  用户名: {username} | 权限等级: {permission_level}")

    return test_info, train_info

# 指定要搜索的目录
directory_to_search = r'.\voice'

# 获取按前缀分组的文件列表
# files_by_prefix = get_files_with_prefix_count(directory_to_search)
files_by_prefix = get_files_by_parent_folder(directory_to_search)


# 生成测试集和训练集信息
test_info, train_info = generate_test_and_train_info(files_by_prefix)

# 将测试集文件信息写入 CSV 文件
test_csv_file_path = r'.\Test_003.csv'
with open(test_csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['filename'])
    writer.writeheader()  # Write the header row
    for info in test_info:
        writer.writerow(info)

# 将训练集文件信息写入 CSV 文件
train_csv_file_path = r'.\Train_003.csv'
with open(train_csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['filename', 'username', 'permission_level'])
    writer.writeheader()  # Write the header row
    for info in train_info:
        writer.writerow(info)

print(f"Test file list has been written to {test_csv_file_path}")
print(f"Training file list with info has been written to {train_csv_file_path}")
