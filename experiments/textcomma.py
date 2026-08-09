from paddlespeech.cli.text.infer import TextExecutor
text_punc = TextExecutor()
result = text_punc(text=input("Enter text: "))
print(result)

