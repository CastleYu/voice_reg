import base64
import logging
import hashlib

# 设置日志格式和级别
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s')

# 使用的固定字符集（只包含大小写字母和数字）
CHAR_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
SEP = '|'


def encode_string(input_string):
    """
    将原始字符串编码为仅由固定字符集组成的字符串
    """
    # 使用Base64编码，并将其转换为仅包含字符集的编码
    encoded = base64.urlsafe_b64encode(input_string.encode()).decode()
    return encoded


def decode_string(encoded_string):
    """
    解码仅由固定字符集组成的字符串还原原始字符串
    """
    decoded = base64.urlsafe_b64decode(encoded_string.encode()).decode()
    return decoded


def encode(string_list):
    """
    将多个字符串编码为一个定长的可逆字符串
    """
    # 使用不可冲突的分隔符（此处选用双下划线）
    separator = SEP

    # 编码每个字符串并用分隔符连接
    encoded_strings = [encode_string(s) for s in string_list]
    joined_string = separator.join(encoded_strings)

    # 添加校验和及字符串个数信息
    string_count = len(string_list)
    checksum = hashlib.md5(joined_string.encode()).hexdigest()[:8]  # 取MD5的前8位作为校验和

    # 拼接字符串个数和校验和
    full_string = f"{string_count}{separator}{checksum}{separator}{joined_string}"

    # 定长编码（假设为64个字符长度）
    final_encoded = base64.urlsafe_b64encode(full_string.encode()).decode()

    return final_encoded


def decode(encoded):
    """
    将定长可逆字符串解码为原始字符串列表
    """
    separator = SEP

    # Base64解码
    full_string = base64.urlsafe_b64decode(encoded.encode()).decode()

    # 提取字符串个数和校验和
    parts = full_string.split(separator, 2)
    string_count = int(parts[0])
    checksum = parts[1]
    joined_string = parts[2]

    # 校验和验证
    calculated_checksum = hashlib.md5(joined_string.encode()).hexdigest()[:8]
    if calculated_checksum != checksum:
        logging.error("校验和不匹配！原始校验和: %s, 计算校验和: %s", checksum, calculated_checksum)
        raise ValueError("校验和不匹配，解码失败")

    # 分隔符拆分得到原始字符串
    encoded_strings = joined_string.split(separator)
    if len(encoded_strings) != string_count:
        logging.error("字符串数量不匹配！预期数量: %d, 实际数量: %d", string_count, len(encoded_strings))
        raise ValueError("字符串数量不匹配，解码失败")

    # 解码每个字符串
    decoded_strings = [decode_string(s) for s in encoded_strings]

    return decoded_strings


# 用例测试
if __name__ == "__main__":
    original_strings = ["17289879887", "1234562890"]
    logging.info("原始字符串: %s", original_strings)

    encoded = encode(original_strings)
    logging.info("编码后的定长字符串: %s (%d)", encoded, len(encoded))

    decoded = decode(encoded)
    logging.info("解码后的字符串列表: %s", decoded)

    assert decoded == original_strings, "解码后的结果与原始字符串不一致"
    logging.info("测试通过！")
