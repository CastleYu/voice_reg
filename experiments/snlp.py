from snownlp import SnowNLP

# 定义肯定词汇和拒绝词汇
affirmative_words = ['是的', '当然', '肯定', '好']
negative_words = ['不']


def check_sentiment(word):
    # 检查是否是肯定词汇
    if word in affirmative_words:
        return "肯定情感"
    # 检查是否是拒绝词汇
    elif word in negative_words:
        return "拒绝情感"
    # 如果都不是，则进行一般情感分析
    else:
        s = SnowNLP(word)
        sentiment = s.sentiments
        if sentiment > 0.5:
            return f"+{sentiment:.2}"
        else:
            return f"-{sentiment:.2}"


# 测试几个词汇
test_words = ['开门', '不', '高兴', '悲伤', "不可以", "绝不", "别", "不要", "禁止", "拒绝接受"]
results = {word: check_sentiment(word) for word in test_words}
print(results)
