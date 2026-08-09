from abc import ABC, abstractmethod

import paddle
# noinspection PyPackageRequirements
from paddlespeech.cli.asr import ASRExecutor

from wrappers.timer import timerC


# from paddlespeech.cli.text import TextExecutor


# 适配器
class SpeechRecognitionAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def recognize(self, audio_file, lang='zh', sample_rate=16000):
        return self.adaptee.recognize(audio_file, lang, sample_rate)


# PaddleSpeech实现类
class PaddleSpeechRecognition:
    def __init__(self):
        self.asr_executor = ASRExecutor()
        # self.text_executor = TextExecutor()

    @timerC
    def recognize(self, audio_file, lang, sample_rate):
        voice_text = self.asr_executor(
            model='conformer_wenetspeech',
            lang=lang,
            sample_rate=sample_rate,
            config=None,
            ckpt_path=None,
            audio_file=audio_file,
            force_yes=True,
            device=paddle.get_device())
        return voice_text


if __name__ == '__main__':
    from ui_runner import FileDropApp

    FileDropApp(SpeechRecognitionAdapter(PaddleSpeechRecognition()).recognize).run()
