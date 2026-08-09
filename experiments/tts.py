from paddlespeech.cli.tts.infer import TTSExecutor

tts = TTSExecutor()
text = input("输入声音:")
tts(text=text, output=f"{text}.wav")
