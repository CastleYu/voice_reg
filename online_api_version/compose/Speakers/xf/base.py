import base64
import hashlib
import hmac
import traceback
import urllib.parse
import urllib.parse
from datetime import datetime, timezone

import websocket


class XFYun:
    def __init__(self, host, api_key, api_secret):
        self.host = host
        self.api_secret = api_secret
        self.api_key = api_key

    # @property
    # def _auth_url(self):
    #     # 解析 URL
    #     ul = urllib.parse.urlparse(self.host)
    #
    #     # 签名时间，格式为 RFC1123
    #     date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    #
    #     # 参与签名的字段 host, date, request-line
    #     sign_string = "\n".join([
    #         f"host: {ul.hostname}",
    #         f"date: {date}",
    #         f"GET {ul.path} HTTP/1.1"
    #     ])
    #
    #     # 生成签名结果
    #     sha = hmac.new(self.api_secret.encode('utf-8'),
    #                    sign_string.encode('utf-8'),
    #                    hashlib.sha256).digest()
    #     signature = base64.b64encode(sha).decode('utf-8')
    #
    #     # 构建请求参数
    #     auth_url = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'
    #
    #     # 将请求参数使用 Base64 编码
    #     authorization = base64.b64encode(auth_url.encode('utf-8')).decode('utf-8')
    #
    #     # 将参数拼接为 URL 编码格式
    #     query_params = urllib.parse.urlencode({
    #         "host": ul.hostname,
    #         "date": date,
    #         "authorization": authorization
    #     })
    #
    #     # 最终的完整 URL
    #     callurl = f"{self.host}?{query_params}"
    #     return callurl

    @property
    def auth_url(self):
        # 解析 URL
        ul = urllib.parse.urlparse(self.host)

        # 签名时间，格式为 RFC1123
        date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        # 参与签名的字段 host, date, request-line
        sign_string = "\n".join([
            f"host: {ul.hostname}",
            f"date: {date}",
            f"GET {ul.path} HTTP/1.1"
        ])

        # 生成签名结果
        sha = hmac.new(self.api_secret.encode('utf-8'),
                       sign_string.encode('utf-8'),
                       hashlib.sha256).digest()
        signature = base64.b64encode(sha).decode('utf-8')

        # 构建请求参数
        auth_url = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature}"'

        # 将请求参数使用 Base64 编码
        authorization = base64.b64encode(auth_url.encode('utf-8')).decode('utf-8')

        query_params = {
            "host": ul.hostname,
            "date": date,
            "authorization": authorization
        }
        encoded_params = "&".join(
            f"{urllib.parse.quote_plus(k)}={urllib.parse.quote(v, safe='')}" for k, v in query_params.items()
        )

        # 最终的完整 URL
        callurl = f"{self.host}?{encoded_params}"
        return callurl


import websocket
import ssl


class WS:
    def __init__(self):
        self.app: websocket.WebSocketApp = None
        self.is_opened = False

    def _on_open(self, ws):
        """默认的连接建立成功回调"""
        print("WebSocket connection opened.")
        self.is_opened = True

    def _on_message(self, ws, message):
        """默认的消息接收回调"""
        print(f"Received message: {message}")

    def _on_error(self, ws, error):
        """默认的错误回调"""
        traceback.print_exc()
        # print(f"WebSocket error occurred: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """默认的连接关闭回调"""
        print(f"WebSocket connection closed: code={close_status_code}, message={close_msg}")
        self.is_opened = False

    def open(self,
             host,
             on_open=None,
             on_msg=None,
             on_err=None,
             on_close=None):
        # 如果没有提供自定义回调，则使用默认回调
        self.app = websocket.WebSocketApp(
            host,
            on_open=on_open or self._on_open,
            on_message=on_msg or self._on_message,
            on_error=on_err or self._on_error,
            on_close=on_close or self._on_close
        )
        self.app.on_open = on_open
        # 启动
        self.app.run_forever(sslopt={
            "cert_reqs": ssl.CERT_NONE})
