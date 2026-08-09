<template>
  <div class="w-full min-h-screen bg-gradient-to-br from-gray-100 to-blue-200 flex items-center justify-center p-6">
    <div class="w-full max-w-xl md:max-w-3xl lg:max-w-4xl bg-white rounded-xl shadow-lg overflow-hidden">
      <!-- 标题部分 -->
      <div class="p-6 border-b border-gray-200 bg-blue-600 text-white text-center rounded-t-xl">
        <h1 class="text-4xl font-extrabold">智能家居语音指令处理系统</h1>
      </div>

      <!-- 内容部分 -->
      <div class="p-8 space-y-8">
        <!-- 录音按钮 -->
        <button
            @click="toggleListening"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-xl text-lg shadow-md transition duration-300 ease-in-out flex items-center justify-center"
            :class="{ 'bg-red-600 hover:bg-red-700': isListening }"
        >
          <Mic v-if="!isListening" class="mr-2 h-6 w-6"/>
          <MicOff v-else class="mr-2 h-6 w-6"/>
          {{ isListening ? '停止录音' : '开始录音' }}
        </button>

        <!-- 上传录音 -->
        <div>
          <label class="block text-sm font-medium text-gray-700">上传本地录音文件:</label>
          <input
              type="file"
              accept="audio/*"
              @change="uploadAudio"
              class="mt-2 block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100"
          />
        </div>

        <!-- 状态 -->
        <div class="flex flex-col items-center bg-gray-50 p-6 rounded-lg shadow-sm">
          <span class="text-sm font-medium text-gray-600">状态:</span>
          <span class="text-base font-semibold text-gray-800">{{ status }}</span>
        </div>

        <!-- 用户语音 -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">您说:</h3>
          <p class="text-gray-800">{{ transcript || '(尚未识别到语音)' }}</p>
        </div>

        <!-- 系统响应 -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">系统响应:</h3>
          <p class="text-gray-800">{{ response || '(等待指令)' }}</p>
        </div>

        <!-- 设备和操作 -->
        <div class="p-6 bg-gray-50 rounded-lg shadow-sm">
          <h3 class="text-sm font-semibold text-gray-700 mb-2">操作信息:</h3>
          <p class="text-gray-800"><strong>设备:</strong> {{ deviceName || '(等待指令)' }}</p>
          <p class="text-gray-800"><strong>功能:</strong> {{ operationDescription || '(等待指令)' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import {Mic, MicOff} from 'lucide-vue-next';
import axios from 'axios';

const isListening = ref(false);
const transcript = ref('');
const response = ref('');
const status = ref('就绪');
const deviceName = ref('');
const operationDescription = ref('');
const audioChunks = ref([]);
let mediaRecorder = null; // 使用 let 而不是 ref，因为 MediaRecorder 不是响应式的

const toggleListening = async () => {
  if (isListening.value) {
    stopRecording();
  } else {
    await startRecording();
  }
};

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    mediaRecorder = new MediaRecorder(stream, {mimeType: 'audio/webm'});

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data);
      }
    };

    mediaRecorder.onstop = () => {
      saveRecording();
    };

    mediaRecorder.start();
    isListening.value = true;
    status.value = '正在录音...';
  } catch (error) {
    console.error('录音失败:', error);
    status.value = '无法录音，请检查权限';
  }
};

const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    isListening.value = false;
    status.value = '录音已停止，正在上传...';
  }
};

const saveRecording = () => {
  if (audioChunks.value.length === 0) {
    status.value = '没有录音数据';
    return;
  }

  // 将音频数据转换为 Blob 然后上传录音文件
  const audioBlob = new Blob(audioChunks.value, {type: 'audio/webm'}); // 使用与 MediaRecorder 相同的 MIME 类型
  const audioFile = new File([audioBlob], 'recording.webm', {type: 'audio/webm'});
  uploadAudio({target: {files: [audioFile]}});

  audioChunks.value = [];
};

const uploadAudio = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  status.value = '上传中...';
  const formData = new FormData();
  formData.append('file', file);

  try {
    const {data} = await axios.post('http://localhost:5000/stt', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    transcript.value = data.text;
    await handleCommand(transcript.value);
    status.value = '就绪';
  } catch (error) {
    status.value = '上传失败，请重试';
    console.error(error);
  }
};

const handleCommand = async (command) => {
  try {
    const {data} = await axios.post('http://localhost:5000/parse_command', {
      command,
    });
    response.value = `解析成功: ${data.parsed_command.name}`;
    parseResponse(data.parsed_command);
  } catch (error) {
    response.value = '未解析到相关指令';
    console.error(error);
  }
};

const parseResponse = (data) => {
  console.log(data);
  let parsedData = {};
  try {
    parsedData = JSON.parse(data.arguments || '{}');
  } catch (e) {
    console.error('解析 JSON 失败:', e);
  }
  deviceName.value = data.name || '未知设备';
  const action = parsedData.action;
  operationDescription.value = `操作指令：${action || '未知'}，位置：${parsedData.location || '未知位置'}`;
};
</script>
