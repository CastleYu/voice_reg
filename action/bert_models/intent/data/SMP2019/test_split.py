import json
from sklearn.model_selection import train_test_split

# 读取JSON数据集
def load_json_data(file_path):
    """从JSON文件加载数据"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 将数据集划分为训练集和测试集
def split_dataset(data, test_size=0.2, random_state=42):
    """划分训练集和测试集"""
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)
    return train_data, test_data

# 保存分割后的数据集到文件
def save_json_data(data, file_path):
    """保存数据到JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def main():
    # 定义文件路径
    input_file = 'data.json'  # 原始数据集文件
    train_output_file = 'train.json'  # 保存训练集的文件
    test_output_file = 'test.json'  # 保存测试集的文件

    # 加载数据集
    data = load_json_data(input_file)

    # 划分数据集
    train_data, test_data = split_dataset(data, test_size=0.2)

    # 保存训练集和测试集
    save_json_data(train_data, train_output_file)
    save_json_data(test_data, test_output_file)

    print(f"训练集大小: {len(train_data)}")
    print(f"测试集大小: {len(test_data)}")

if __name__ == "__main__":
    main()
