# -*- coding:utf-8 -*-
import json
import random
import pandas as pd
from detector import JointIntentSlotDetector
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import time

# 记录时间
start1_time = time.perf_counter()

# 加载模型
model = JointIntentSlotDetector.from_pretrained(
    model_path='save_model_2/bert-base-chinese',
    tokenizer_path='save_model_2/bert-base-chinese',
    intent_label_path='data/SMP2019/intent_labels.txt',
    slot_label_path='data/SMP2019/slot_labels.txt'
)

start2_time = time.perf_counter()

# 加载测试数据
with open("data/SMP2019/test.json", 'r', encoding='utf-8') as f:
    lines = json.load(f)

# 初始化变量用于存储结果
all_text = []
pred_intents = []
true_intents = []
pred_slots = []
true_slots = []

# 遍历所有样本
for line in lines:
    pred = model.detect(line['text'].strip())
    expect = line

    # 将预测和真实结果记录下来
    pred_intents.append(pred['intent'])
    true_intents.append(expect['intent'])
    pred_slots.append(pred['slots'])
    true_slots.append(expect['slots'])

    # 如果意图预测错误，打印对比信息
    if pred['intent'] != expect['intent']:
        if pred['slots'] != expect['slots']:
            print("预测结果:", pred)
            print("期望结果:", expect)
        else:
            print("意图预测错误，但槽位正确:", line['text'])
        print()

# 评估四个指标：准确率、精确率、召回率和F1-score
intent_accuracy = accuracy_score(true_intents, pred_intents)
intent_precision = precision_score(true_intents, pred_intents, average='weighted')
intent_recall = recall_score(true_intents, pred_intents, average='weighted')
intent_f1 = f1_score(true_intents, pred_intents, average='weighted')

print(f"意图识别 - \nAccuracy: {intent_accuracy:.4f}, \nPrecision: {intent_precision:.4f}, \nRecall: {intent_recall:.4f}, \nF1 Score: {intent_f1:.4f}")

# 注意：槽位评估需要基于每个槽的标签
slot_accuracy = accuracy_score(true_slots, pred_slots)
slot_precision = precision_score(true_slots, pred_slots, average='weighted')
slot_recall = recall_score(true_slots, pred_slots, average='weighted')
slot_f1 = f1_score(true_slots, pred_slots, average='weighted')

print(f"槽位识别 - 准确率: {slot_accuracy:.4f}, 精确率: {slot_precision:.4f}, 召回率: {slot_recall:.4f}, F1分数: {slot_f1:.4f}")

# 记录时间
end_time = time.perf_counter()
time1 = (end_time - start1_time)
time2 = (end_time - start2_time)

# 输出时间信息和平均处理时间
print("所有检测时间（包括加载模型）：", time1, "s",
      "除去模型加载时间：", time2, "s",
      "总预测数据量：", len(all_text),
      "平均预测一条的时间（除去加载模型）：", time2 / len(lines), "s/条")
