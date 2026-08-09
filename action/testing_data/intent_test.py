import json

from action.intent_recg import IntentRecognition


class IntentRecognitionTest(IntentRecognition):
    def __init__(self, model_path, intent_label_path, slot_label_path):
        IntentRecognition.__init__(self, model_path, intent_label_path, slot_label_path)

    def run_test_cases(self, test_data_path):
        """运行测试集并输出不匹配的预测"""
        with open(test_data_path, 'r', encoding='utf-8') as f:
            lines = json.load(f)

        mismatches = []
        total_detect_time = 0

        for line in lines:
            pred, detect_time = self.detect_intent(line['text'])
            total_detect_time += detect_time
            expect = line
            if pred['intent'] != expect['intent'] or pred['slots'] != expect['slots']:
                mismatches.append({
                    'predicted': pred,
                    'expected': expect,
                    'text': line['text']})

        avg_time = total_detect_time / len(lines) if lines else 0
        return mismatches, total_detect_time, avg_time

    def print_detection_time(self, text):
        """输出检测时间"""
        prediction = self.detect_intent(text)
        print(f"检测结果：{prediction}")
        # print(f"检测时间（不包括加载时间）：{detect_time:.4f}秒")

    def print_summary(self, num_cases, detect_time):
        """输出检测时间统计信息"""
        print(f"所有检测时间（包括加载模型）：{self.load_time + detect_time:.4f}秒")
        print(f"除去模型加载时间：{detect_time:.4f}秒")
        print(f"总预测数据量：{num_cases}")
        print(f"平均预测一条的时间（除去加载模型）：{detect_time / num_cases:.4f}秒/条" if num_cases else "无预测数据")


# 示例使用
if __name__ == "__main__":
    intent_recognizer = IntentRecognitionTest(
        model_path='../bert_models/intent',
        intent_label_path='../bert_models/intent/data/SMP2019/intent_labels.txt',
        slot_label_path='../bert_models/intent/data/SMP2019/slot_labels.txt'
    )

    # 单条检测
    print(intent_recognizer.detect_intent("我要打开财务报表"))

    # 批量检测，统计时间并输出不匹配项
    # mismatches, total_detect_time, avg_time = intent_recognizer.run_test_cases("./bert_models/intent/data/SMP2019/test.json")
    # intent_recognizer.print_summary(len(mismatches), total_detect_time)
    #
    # if mismatches:
    #     print("以下测试用例的预测与预期不匹配：")
    #     for mismatch in mismatches:
    #         print(f"文本: {mismatch['text']}")
    #         print(f"预测: {mismatch['predicted']}")
    #         print(f"预期: {mismatch['expected']}\n")
