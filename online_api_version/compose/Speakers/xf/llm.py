import requests

from service.device import function_list

if __name__ == '__main__':
    from config import LLMConfig as cfg
else:
    from .config import LLMConfig as cfg


class SparkAIVersion:
    HttpHOST = "https://spark-api-open.xf-yun.com/v1/chat/completions"
    SparkLite = ('wss://spark-api.xf-yun.com/v1.1/chat', 'lite')
    SparkPro = ('wss://spark-api.xf-yun.com/v3.1/chat', 'generalv3')
    SparkPro128K = ('wss://spark-api.xf-yun.com/chat/pro-128k', 'pro-128k')
    SparkMax = ('wss://spark-api.xf-yun.com/v3.5/chat', 'generalv3.5')
    SparkMax32K = ('wss://spark-api.xf-yun.com/chat/max-32k', 'max-32k')
    Spark4Ultra = ('wss://spark-api.xf-yun.com/v4.0/chat', '4.0Ultra')


class XFSparkAI:
    def __init__(self,
                 max_tokens=4096,
                 top_k=4,
                 temperature=0.5,
                 default_prompt='',
                 function_list=None):
        self.host = SparkAIVersion.HttpHOST
        self.header = {
            "Authorization": cfg.BEARER
        }
        self.max_tokens = max_tokens
        self.top_k = top_k
        self.temperature = temperature
        self.prompt: str = default_prompt
        self.msg_list = [
            {
                "role": "system",
                "content": self.prompt
            }
        ]
        if function_list is not None:
            self.load_function(function_list)
        else:
            self.functions = None

    def load_function(self, function_list):
        self.functions = [
            {
                "function": i,
                "type": "function"
            } for i in function_list]
        return self

    def add_prompt(self, prompt: str):
        if not prompt.startswith('\n') and not self.prompt.endswith('\n'):
            self.prompt += '\n'
        self.prompt += prompt
        self.msg_list[0] = {
            "role": "system",
            "content": self.prompt
        }
        return self

    def add_chat(self, msg: str):
        self.msg_list.append(
            {
                "role": "user",
                "content": msg
            }
        )
        return self

    def add_bot(self, msg: str):
        self.msg_list.append(
            {
                "role": "assistant",
                "content": msg
            }
        )
        return self

    def add_system(self, msg: str):
        self.msg_list.append(
            {
                "role": "system",
                "content": msg
            }
        )

    def send(self, msg=None, max_tokens=None, top_k=None, temperature=None):
        if msg is not None:
            self.msg_list.append(
                {
                    "role": "user",
                    "content": msg
                }
            )
        data = {
            "max_tokens": max_tokens or self.max_tokens,
            "top_k": top_k or self.top_k,
            "temperature": temperature or self.temperature,
            "messages": self.msg_list,
            "model": SparkAIVersion.Spark4Ultra[1],
            'stream': False
        }
        if self.functions is not None:
            data['tools'] = self.functions
        response = requests.post(self.host, headers=self.header, json=data, stream=True)
        response.encoding = "utf-8"
        try:
            import json
            resp_dict = json.loads(response.text)
            func_call = resp_dict['choices'][0]['message']['tool_calls']['function']
            return func_call
        except KeyError:
            import json
            try:
                resp_dict = json.loads(response.text)
                print(resp_dict['choices'][0]['message']['content'])
            except json.decoder.JSONDecodeError or KeyError:
                print(response.text)
            return None


llm = XFSparkAI()

llm.load_function(function_list)
if __name__ == '__main__':
    print(llm.send("翻译下列文本到中文：ボクサー娘とイチャラブボクシング"))
