from textblob import TextBlob


def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 至 1 之间的值，负值表示否定，正值表示肯定
    return sentiment


# 示例
print(analyze_sentiment('这是好的'))  # 输出可能为 '肯定'
print(analyze_sentiment('不'))  # 输出可能为 '否定'
print(analyze_sentiment('这是一本书'))  # 输出可能为 '中性'
