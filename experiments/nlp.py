from time import perf_counter

import jieba
from LAC import LAC

start1_time = perf_counter()
# 初始化LAC分词器
lac = LAC(mode='lac')

# 定义指令库
commands = {
    '开门': ['开门', '开启门', '把门打开', '请开门'],
    '开锁': ['开锁', '解锁', '把锁打开', '请开锁'],
    '打开报表': ['打开报表', '生成报表', '查看报表', '展示报表']
}


# 打开|开启 + 门
# 开门

# 预处理函数
def preprocess_text(text):
    # 使用LAC进行分词和词性标注
    lac_result = lac.run(text)
    print(lac_result)
    print(dict((lac_result[0], lac_result[1])))
    words = lac_result[0]  # 分词结果
    print(words)
    return ' '.join(words)


# 匹配函数
def match_command(text, commands):
    preprocessed_text = preprocess_text(text)
    for command, variations in commands.items():
        for variation in variations:
            if variation in preprocessed_text:
                return command
    return None


# 测试

start2_time = perf_counter()
print(start2_time - start1_time)
input_text = "能不能不要吵了，把门打开，打开一个报表"
matched_command = match_command(input_text, commands)
end1_time = perf_counter()
print(end1_time - start2_time)
words = jieba.cut(input_text, cut_all=False)
print(list(words))
end2_time = perf_counter()
print(end2_time - end1_time)
if matched_command:
    print(f"识别到的指令: {matched_command}")
else:
    print("未识别到有效指令")
