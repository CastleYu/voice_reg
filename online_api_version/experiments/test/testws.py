
import requests

if __name__ == '__main__':
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    data = {
        "max_tokens": 4096,
        "top_k": 4,
        "temperature": 0.5,
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": "今天天气怎么样"
            }
        ],
        "model": "4.0Ultra",
        "tools": [

        ]
    }
    data["stream"] = True
    header = {
        "Authorization": "Bearer OHNqPcNqfdZcXxNGIbsn:JOFlqKKcTLSFJokdAWTb"
    }
    response = requests.post(url, headers=header, json=data, stream=True)

    # 流式响应解析示例
    response.encoding = "utf-8"
    for line in response.iter_lines(decode_unicode="utf-8"):
        print(line)
    