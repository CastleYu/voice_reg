# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#   封装科大讯飞 WebSocket TTS 服务为模块工具库，支持MP3格式输出

import websocket
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import os
import ssl
import threading


class XfTTS:
    def __init__(self, app_id, api_key, api_secret, voice="xiaoyan", encoding="utf8"):
        """
        初始化语音合成模块
        :param app_id: 科大讯飞的应用ID
        :param api_key: 科大讯飞的API密钥
        :param api_secret: 科大讯飞的API密钥
        :param voice: 发音人
        :param encoding: 文本编码格式，默认UTF-8
        """
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.voice = voice
        self.encoding = encoding
        self.output_file = "./output.mp3"  # 设置输出文件为MP3格式

    def _create_url(self):
        """
        生成WebSocket的鉴权URL
        :return: 鉴权后的URL
        """
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = f"host: ws-api.xfyun.cn\ndate: {date}\nGET /v2/tts HTTP/1.1"
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
        )
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        return url + '?' + urlencode(v)

    def synthesize(self, text):
        """
        合成语音并保存为MP3文件
        :param text: 需要合成的文本内容
        """

        class WsParam:
            def __init__(self, app_id, api_key, api_secret, text):
                self.CommonArgs = {
                    "app_id": app_id}
                self.BusinessArgs = {
                    "aue": "lame",
                    "auf": "audio/L16;rate=16000",
                    "vcn": "xiaoyan",
                    "tte": "utf8"}
                self.Data = {
                    "status": 2,
                    "text": str(base64.b64encode(text.encode("utf-8")), "utf8")}

        def on_message(ws, message):
            try:
                message = json.loads(message)
                code = message["code"]
                if code != 0:
                    print("Error:", message["message"])
                    return
                audio = base64.b64decode(message["data"]["audio"])
                with open(self.output_file, 'ab') as f:
                    f.write(audio)
                if message["data"]["status"] == 2:
                    ws.close()
            except Exception as e:
                print("Exception:", e)

        def on_error(ws, error):
            print("Error:", error)

        def on_close(ws):
            print("Connection closed")

        def on_open(ws):
            def run(*args):
                payload = json.dumps({
                    "common": params.CommonArgs,
                    "business": params.BusinessArgs,
                    "data": params.Data,
                })
                if os.path.exists(self.output_file):
                    os.remove(self.output_file)
                ws.send(payload)

            threading.Thread(target=run).start()

        params = WsParam(self.app_id, self.api_key, self.api_secret, text)
        ws_url = self._create_url()
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.on_open = on_open
        ws.run_forever(sslopt={
            "cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    # 测试模块
    app_id = "4834fe29"
    api_key = "OGQyOTcxNDlmMjBkMGVlYjQwODMxNzQ1"
    api_secret = "bc9b188a9506bb31a71a6caf591d30ec"
    text = "这是一个语音合成模块测试示例。"
    tts = XfTTS(app_id, api_key, api_secret)
    tts.synthesize(text)
