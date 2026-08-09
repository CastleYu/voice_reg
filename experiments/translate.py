from paddlespeech.cli.st.infer import STExecutor

st = STExecutor()
result = st(audio_file="./en.wav")
print(result)
