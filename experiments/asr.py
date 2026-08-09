import warnings

from paddlespeech.cli.text import TextExecutor

warnings.filterwarnings('ignore')

from paddlespeech.cli.asr.infer import ASRExecutor

asr = ASRExecutor()
result = asr(
    lang='zh',
    force_yes=True,
    audio_file="zh01.wav"
)

text_punc = TextExecutor()
result = text_punc(text=result)
print(result)
