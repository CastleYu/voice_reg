# -*- coding:utf-8 -*-
import json
import random
import pandas as pd
from detector import JointIntentSlotDetector
import time

start1_time = time.perf_counter()
model = JointIntentSlotDetector.from_pretrained(
    model_path='save_model_2/bert-base-chinese',
    tokenizer_path='save_model_2/bert-base-chinese',
    intent_label_path='data/SMP2019/intent_labels.txt',
    slot_label_path='data/SMP2019/slot_labels.txt'
)
start2_time = time.perf_counter()
# df = pd.read_csv('./lcqmc_test.txt', sep='\t')
# all_text = random.sample(list(df['text_a']), 30)
# with open("data/SMP2019/test.json", 'r', encoding='utf-8') as f:
#     lines = json.load(f)
# all_text = []
# for line in lines:
#     pred = model.detect(line['text'].strip())
#     expect = line
#     if pred['intent'] != expect['intent']:
#         if pred['slots'] != expect['slots']:
#             print(pred)
#             print(expect)
#         else:
#             print(line['text'])
#         print()
print(model.detect("我要打开财务报表"))
end_time = time.perf_counter()
time1 = (end_time - start1_time)
time2 = (end_time - start2_time)
print("所有检测时间（包括加载模型）：", time1, "s", "除去模型加载时间：", time2, "s",
      "总预测数据量：", 1, "平均预测一条的时间（除去加载模型）：", time2 / 1, "s/条")
