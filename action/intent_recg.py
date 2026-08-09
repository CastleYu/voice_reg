# -*- coding:utf-8 -*-
import time

from action.joint.detector import JointIntentSlotDetector
from wrappers.timer import timerC


class IntentRecognition:
    def __init__(self, model_path, intent_label_path, slot_label_path):
        self.model_path = model_path
        self.tokenizer_path = model_path
        self.intent_label_path = intent_label_path
        self.slot_label_path = slot_label_path
        self.model = None
        self.load_time = None
        self._initialize_model()

    def _initialize_model(self):
        self.model = JointIntentSlotDetector.from_pretrained(
            model_path=self.model_path,
            tokenizer_path=self.tokenizer_path,
            intent_label_path=self.intent_label_path,
            slot_label_path=self.slot_label_path
        )

    @timerC
    def detect_intent(self, text):
        """检测输入文本的意图和槽位"""
        if not self.model:
            self._initialize_model()
        return self.model.detect(text.strip())


if __name__ == '__main__':
    intent_recognizer = IntentRecognition(
        model_path='./bert_models/intent',
        intent_label_path='./bert_models/intent/data/SMP2019/intent_labels.txt',
        slot_label_path='./bert_models/intent/data/SMP2019/slot_labels.txt'
    )
    result = intent_recognizer.detect_intent("启动空调")
    command_intent = result['intent']
    # command_slot = result
    print(result)
    
    