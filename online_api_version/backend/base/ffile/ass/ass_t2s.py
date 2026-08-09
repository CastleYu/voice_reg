import ass
import pysubs2
import opencc
from tqdm import tqdm

from base.interact.direc import ask_directory, ask_file, ask_file_list, detect_file_encoding

# 初始化繁体转简体的转换器
converter = opencc.OpenCC('t2s')  # t2s 表示繁体到简体的转换


# 读取并转换 ASS 字幕
def ass_t2s_pysub2(input_file, output_file=None):
    if output_file is None:
        output_file = input_file
    subs = pysubs2.load(input_file, encoding=detect_file_encoding(input_file))

    # 遍历每一个字幕事件
    for line in subs:
        # 转换每一行字幕的文本
        line.text = converter.convert(line.text)

    # 保存转换后的字幕为新的 ASS 文件
    subs.save(output_file, encoding='utf-8')


# 读取 ASS 文件
def ass_t2s_ass(input_file, output_file=None):
    if output_file is None:
        output_file = input_file
    # 打开并解析 ASS 文件
    with open(input_file, 'r', encoding=detect_file_encoding(input_file)) as file:
        doc = ass.parse(file)

    # 遍历字幕事件，并将繁体转换为简体
    for event in doc.events:
        if event.text:
            event.text = converter.convert(str(event.text))

    # 将修改后的字幕写回新的 ASS 文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(doc))


files = ask_file_list()
for file in tqdm(files):
    ass_t2s_pysub2(file)
