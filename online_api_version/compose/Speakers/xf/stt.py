import base64
import json
import os.path
import time

if __name__ == '__main__':
    from audio import AudioProcessor
    from base import XFYun, WS
else:
    from .audio import AudioProcessor
    from .base import XFYun, WS

HOST = "wss://iat-api.xfyun.cn/v2/iat"

PCM = 'raw'
SPEEX8K = 'speex'
SPEEX16K = 'speex-wb'
MP3 = 'lame'


class DataFrameGetter:
    def __init__(self, fp, app_id, sample_rate=16000, frameSize=1280, interval=40, format=PCM):
        """
        初始化 DataFrameGetter
        :param fp: 文件对象
        :param app_id: 应用 ID
        :param sample_rate: 采样率，默认 16000
        :param frameSize: 每帧大小，默认 1280 字节
        :param interval: 每帧发送间隔，单位为毫秒
        :param format: 音频格式，默认 PCM
        """
        self.fp = fp
        self.app_id = app_id
        self.sample_rate = sample_rate
        self.frameSize = frameSize
        self.interval = interval / 1000  # 转换为秒
        self.format = format

    def head(self):
        """
        生成第一帧数据（头帧）
        :return: 第一帧 JSON 字符串
        """
        buf = self.fp.read(self.frameSize)
        data = {
            "common": {
                "app_id": self.app_id,
            },
            "business": {
                "domain": "iat",
                "language": "zh_cn",
                "accent": "mandarin",
                "vinfo": 0,
                "vad_eos": 3000,
                "ptt": 0
            },
            "data": {
                "status": 0,  # 头帧状态
                "format": f"audio/L16;rate={self.sample_rate}",
                "audio": str(base64.b64encode(buf), 'utf-8'),
                "encoding": self.format
            }
        }
        return json.dumps(data)

    def body(self):
        """
        生成器函数，用于生成中间帧数据
        :yield: 中间帧 JSON 字符串
        """
        while True:
            buf = self.fp.read(self.frameSize)
            if not buf:  # 文件结束
                break
            data = {
                "data": {
                    "status": 1,  # 中间帧状态
                    "format": f"audio/L16;rate={self.sample_rate}",
                    "audio": str(base64.b64encode(buf), 'utf-8'),
                    "encoding": self.format
                }
            }
            yield json.dumps(data)
            time.sleep(self.interval)

    def tail(self):
        """
        生成最后一帧数据（尾帧）
        :return: 最后一帧 JSON 字符串
        """
        buf = self.fp.read(self.frameSize)
        data = {
            "data": {
                "status": 2,  # 尾帧状态
                "format": f"audio/L16;rate={self.sample_rate}",
                "audio": str(base64.b64encode(buf), 'utf-8'),
                "encoding": self.format
            }
        }
        return json.dumps(data)


class SpeechRecognitionConfig:
    def __init__(self,
                 language_code: str,  # 语种
                 application_domain: str,  # 应用领域
                 dialect: str,  # 方言
                 silence_duration_ms: int = 2000,  # 静默时长，单位毫秒
                 dynamic_correction: str = None,  # 动态修正
                 personalization_domain: str = None,  # 个性化领域
                 punctuation_enabled: int = 1,  # 是否启用标点符号
                 punctuation_position_mode: int = 1,  # 标点符号返回位置模式
                 character_set: str = "zh-cn",  # 字符集（简体/繁体）
                 frame_offset_info: int = 0,  # 是否返回端点帧偏移值
                 numeric_format: int = 1,  # 数字格式（阿拉伯数字）
                 speex_frame_length: int = None,  # speex音频帧长度
                 sentence_candidates: int = 1,  # 句子多候选数量
                 word_candidates: int = 1):  # 词语多候选数量
        """
        初始化语音识别配置。

        :param language_code: 语种
        :param application_domain: 应用领域
        :param dialect: 方言
        :param silence_duration_ms: 后端点检测静默时间，单位为毫秒，默认为2000
        :param dynamic_correction: 动态修正
        :param personalization_domain: 领域个性化参数
        :param punctuation_enabled: 是否开启标点符号添加，1为开启，0为关闭
        :param punctuation_position_mode: 标点返回位置控制，1为开启，0为关闭
        :param character_set: 字符集
        :param frame_offset_info: 返回子句结果对应的起始和结束端点帧偏移值，1为开启，0为关闭
        :param numeric_format: 返回结果的数字格式规则，1为开启，0为关闭
        :param speex_frame_length: speex音频帧长，仅在speex音频时使用
        :param sentence_candidates: 多候选句子结果，取值范围[1,5]
        :param word_candidates: 多候选词语结果，取值范围[1,5]
        """
        self.language_code = language_code
        self.application_domain = application_domain
        self.dialect = dialect
        self.silence_duration_ms = silence_duration_ms
        self.dynamic_correction = dynamic_correction
        self.personalization_domain = personalization_domain
        self.punctuation_enabled = punctuation_enabled
        self.punctuation_position_mode = punctuation_position_mode
        self.character_set = character_set
        self.frame_offset_info = frame_offset_info
        self.numeric_format = numeric_format
        self.speex_frame_length = speex_frame_length
        self.sentence_candidates = sentence_candidates
        self.word_candidates = word_candidates

    def to_dict(self):
        """
        将配置转换为字典形式，便于接口调用。
        :return: dict
        """
        return {
            "language": self.language_code,
            "domain": self.application_domain,
            "accent": self.dialect,
            "vad_eos": self.silence_duration_ms,
            "dwa": self.dynamic_correction,
            "pd": self.personalization_domain,
            "ptt": self.punctuation_enabled,
            "pcm": self.punctuation_position_mode,
            "rlang": self.character_set,
            "vinfo": self.frame_offset_info,
            "nunum": self.numeric_format,
            "speex_size": self.speex_frame_length,
            "nbest": self.sentence_candidates,
            "wbest": self.word_candidates
        }

    def __repr__(self):
        return f"SpeechRecognitionConfig({self.to_dict()})"


class XFYunSTT(XFYun, WS):
    def __init__(self, app_id, api_key, api_secret):
        """
        初始化科大讯飞语音转文字模块
        """
        super(XFYunSTT, self).__init__(host=HOST, api_key=api_key, api_secret=api_secret)
        super(WS, self).__init__()
        self.app_id = app_id
        self.result = ''
        self.is_opened = False
        # tmp
        self._on_close = None

    def _get_auth_url(self):
        return self.auth_url

    def _on_message(self, ws, message):
        """
        WebSocket消息回调
        """
        data = json.loads(message)
        try:
            # 检查返回码
            if data["code"] == 0:
                # 提取会话ID
                sid = data.get("sid", "N/A")
                # print(f"Session ID: {sid}")

                # 提取听写结果
                result_data = data.get("data", {}).get("result", {})
                status = data.get("data", {}).get("status", "N/A")
                # print(f"Status: {status}")

                # 提取识别的文本
                words = []
                for word_segment in result_data.get("ws", []):
                    for word_info in word_segment.get("cw", []):
                        words.append(word_info.get("w", ""))

                # 拼接识别结果文本
                recognized_text = "".join(words)
                # print(f"Recognized Text: {recognized_text}")
                self.result += recognized_text
                return recognized_text

            else:
                raise ValueError(f"{data['code']}:{data['message']}")
        except KeyError as e:
            print(e)
            print(json.dumps(data, indent=4, ensure_ascii=False))
            input()

    def read_file(self, audio_file):
        def send_audio(ws, audio_file=audio_file):
            if isinstance(audio_file, str):  # 文件路径
                if not os.path.exists(audio_file):
                    raise FileNotFoundError(audio_file)
                if not audio_file.endswith('.pcm'):
                    ap = AudioProcessor(audio_file)
                    pcm_file = ap.set_sample_rate(audio_file + ".pcm")
                else:
                    pcm_file = audio_file
            elif hasattr(audio_file, 'read'):  # 文件对象或字节流
                pcm_file = "temp_audio_file.pcm"
                with open(pcm_file, 'wb') as temp_fp:
                    temp_fp.write(audio_file.read())
            elif isinstance(audio_file, bytes):  # 字节音频数据
                pcm_file = "temp_audio_file.pcm"
                with open(pcm_file, 'wb') as temp_fp:
                    temp_fp.write(audio_file)
            else:
                raise TypeError(f"Unsupported audio_file type: {type(audio_file)}")

            def run(*args):
                with open(pcm_file, 'rb') as fp:
                    frame_getter = DataFrameGetter(fp,
                                                   app_id=self.app_id)

                    # 发送头帧
                    ws.send(frame_getter.head())

                    # 发送中间帧
                    for body_frame in frame_getter.body():  # 生成器
                        ws.send(body_frame)

                    # 发送尾帧
                    ws.send(frame_getter.tail())
                    time.sleep(1)

                if pcm_file == "temp_audio_file.pcm" or pcm_file != audio_file:
                    os.remove(pcm_file)

                ws.close()

            import _thread as thread
            thread.start_new_thread(run, ())

        # 一次性的 WS 连接
        self.result = ''
        super().open(self.auth_url, on_open=send_audio)
        return self.result


if __name__ == "__main__":
    from config import STTConfig as cfg

    file_path = "../test/123_wav.wav"
    stt = XFYunSTT(cfg.APP_ID, cfg.API_KEY, cfg.API_SECRET)
    result = stt.read_file(file_path)
    print(result)
