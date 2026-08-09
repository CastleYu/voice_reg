import websocket
import base64
import hashlib
import hmac
import json
import time
import ssl
import datetime

class XFYunSTT:
    def __init__(self, app_id, api_key, api_secret):
        """
        初始化科大讯飞语音转文字模块
        """
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.host = "wss://iat-api.xfyun.cn/v2/iat"
        self.result = ""

    def _get_auth_url(self):
        """
        生成WebSocket鉴权URL
        """
        now = datetime.datetime.utcnow()
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')  # 严格使用UTC时间

        # 按讯飞文档格式生成签名字符串
        signature_origin = f"host: iat-api.xfyun.cn\ndate: {date}\nGET /v2/iat HTTP/1.1"
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature = base64.b64encode(signature_sha).decode('utf-8')

        # 生成Authorization头
        authorization = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
        )

        # 返回完整URL
        auth_url = f"{self.host}?authorization={authorization}&date={date}&host=iat-api.xfyun.cn"
        return auth_url

    def _on_message(self, ws, message):
        """
        WebSocket消息回调
        """
        data = json.loads(message)
        if data['code'] == 0:
            result = ''.join([item['w'] for item in data['data']['result']['ws']])
            self.result += result
        else:
            print(f"Error: {data['message']}")

    def _on_error(self, ws, error):
        """
        WebSocket错误回调
        """
        print(f"WebSocket Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """
        WebSocket关闭回调
        """
        print("WebSocket closed")

    def _on_open(self, ws, audio_file):
        """
        WebSocket连接成功后发送音频数据
        """
        def send_data():
            frame_size = 1280  # 每帧大小
            interval = 0.04   # 每帧发送间隔
            with open(audio_file, 'rb') as f:
                while True:
                    data = f.read(frame_size)
                    if not data:
                        break
                    ws.send(json.dumps({
                        "data": {
                            "status": 1 if len(data) < frame_size else 0,
                            "audio": base64.b64encode(data).decode('utf-8'),
                            "format": "audio/L16;rate=16000",
                            "encoding": "raw"
                        }
                    }))
                    time.sleep(interval)
            ws.send(json.dumps({"data": {"status": 2}}))  # 发送结束帧

        send_data()

    def recognize(self, audio_file):
        """
        进行语音识别
        """
        url = self._get_auth_url()
        ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=lambda ws: self._on_open(ws, audio_file)
        )
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self.result

# 使用示例
if __name__ == "__main__":
    # 替换为你的API密钥和应用ID
    app_id = "4834fe29"
    api_secret = "OGQyOTcxNDlmMjBkMGVlYjQwODMxNzQ1"
    api_key = "bc9b188a9506bb31a71a6caf591d30ec"

    stt = XFYunSTT(app_id, api_key, api_secret)
    text = stt.recognize("123_wav.wav")
    print(f"识别结果: {text}")
