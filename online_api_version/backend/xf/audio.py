from pydub import AudioSegment


class AudioProcessor:
    def __init__(self, file_path):
        """
        初始化音频处理类
        :param file_path: 输入音频文件路径
        """
        self.file_path = file_path
        self.audio = AudioSegment.from_file(file_path)

    def get_sample_rate(self) -> int:
        """
        获取音频文件的采样率
        """
        return self.audio.frame_rate

    def set_sample_rate(self, output_path, target_rate=16000):
        audio = self.audio.set_frame_rate(target_rate)
        # 单声道
        audio = audio.set_channels(1)
        audio.export(output_path, format="s16le", codec="pcm_s16le")
        # print(f"音频已调整为单声道，采样率 {target_rate} Hz，文件保存至: {output_path}")
        return output_path

    def get_frame_size(self, interval_ms=40):
        """
        根据音频文件自动计算 frameSize。
        """
        sample_rate = self.audio.frame_rate  # 采样率
        sample_width = self.audio.sample_width  # 每个采样点的字节数（位深度/8）
        channels = self.audio.channels  # 通道数
        bytes_per_ms = sample_rate * sample_width * channels / 1000  # 每毫秒字节数

        frame_size = int(bytes_per_ms * interval_ms)  # interval_ms 毫秒对应的字节数
        return frame_size
