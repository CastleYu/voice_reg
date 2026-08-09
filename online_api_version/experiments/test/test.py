import json
from service.device import function_list

import requests

if __name__ == '__main__':
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    functions = [
        {
            "function": i,
            "type": "function"
        } for i in function_list]

    data = {
        "max_tokens": 256,
        "top_k": 4,
        "temperature": 0.5,
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": "把灯调亮一些"
            }
        ],
        "model": "4.0Ultra",
        "tools": functions,
        "stream": False}
    header = {
        "Authorization": "Bearer OHNqPcNqfdZcXxNGIbsn:JOFlqKKcTLSFJokdAWTb"
    }
    response = requests.post(url, headers=header, json=data, stream=True)
    # 流式响应解析示例
    response.encoding = "utf-8"
    resp: dict = response.json()
    try:
        func_call = resp['choices'][0]['message']['tool_calls']['function']
        print(func_call)
    except KeyError:
        print(json.dumps(resp,indent=4,ensure_ascii=False))
