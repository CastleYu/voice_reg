from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

from vector import *


class AudioVerificationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.deep_speaker = PaddleSpeakerVerification()  # 传入你的模型权重路径

    def initUI(self):
        self.setWindowTitle('Audio Verification')
        self.setGeometry(100, 100, 400, 200)

        # 设置布局
        layout = QVBoxLayout()

        # 结果显示标签
        self.result_label = QLabel("Select two audio files to compare", self)
        layout.addWidget(self.result_label)

        # 选择第一个音频文件按钮
        self.button1 = QPushButton('Select Audio File 1', self)
        self.button1.clicked.connect(self.select_audio_file1)
        layout.addWidget(self.button1)

        # 选择第二个音频文件按钮
        self.button2 = QPushButton('Select Audio File 2', self)
        self.button2.clicked.connect(self.select_audio_file2)
        layout.addWidget(self.button2)

        # 比较按钮
        self.compare_button = QPushButton('Compare', self)
        self.compare_button.clicked.connect(self.compare_audio_files)
        layout.addWidget(self.compare_button)

        self.setLayout(layout)

        self.audio_file1 = None
        self.audio_file2 = None

    def select_audio_file1(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select First Audio File", "", "Audio Files (*.wav *.mp3)",
                                              options=options)
        if file:
            self.audio_file1 = file
            self.result_label.setText(f"Selected Audio File 1: {file}")

    def select_audio_file2(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Second Audio File", "", "Audio Files (*.wav *.mp3)",
                                              options=options)
        if file:
            self.audio_file2 = file
            self.result_label.setText(f"Selected Audio File 2: {file}")

    def compare_audio_files(self):
        if self.audio_file1 and self.audio_file2:
            # 获取音频文件的嵌入向量
            embedding1 = self.deep_speaker.get_embedding_from_file(self.audio_file1)
            embedding2 = self.deep_speaker.get_embedding_from_file(self.audio_file2)

            # 计算它们的相似度
            similarity_score = self.deep_speaker.get_embeddings_score(embedding1, embedding2)
            self.result_label.setText(f"Cosine Similarity: {similarity_score}")
        else:
            self.result_label.setText("Please select both audio files first.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioVerificationApp()
    ex.show()
    sys.exit(app.exec_())
