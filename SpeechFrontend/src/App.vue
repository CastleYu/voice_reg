<template>
  <div id="app">
    <el-container v-loading="isUploading">
      <!-- 顶栏 -->
      <el-header>
        <h1>Speech</h1>
      </el-header>


      <el-main>
        <div
            style="
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 20px;
          "
        >

          <!-- <el-button
            type="primary"
            @click="chooseAudio"
            readonly
            style="flex-grow: 1; margin-left: 20px"
            >选择</el-button
          > -->
          <!-- 识别按钮 -->
          <el-button
              type="warning"
              @click="recognize"
              style="flex-grow: 1; margin-left: 10px"
              icon="el-icon-search"
          >识别
          </el-button
          >
          <!-- 声纹识别按钮 -->
          <!--          <el-button type="primary" @click="recognizeAudioprint" style="flex-grow: 1; margin-left: 10px"-->
          <!--                     icon="el-icon-microphone">声纹识别-->
          <!--          </el-button>-->
          <el-input
              v-model="info"
              placeholder="信息显示"
              readonly
              style="flex-grow: 1; margin-left: 30px"
          ></el-input>
          <!-- 唤醒按钮 -->
          <el-button
              type="success"
              @click="goToRecordingPage"
              style="flex-grow: 1; margin-left: 10px"
              icon="el-icon-microphone"
          >唤醒
          </el-button
          >
        </div>
        <el-row :gutter="20">
          <!-- user列表 -->
          <el-col :span="12">
            <el-card>
              <div
                  style="
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  position: relative;
                "
              >
                <h2 style="flex-grow: 0; text-align: center; margin: 0">
                  用户列表
                </h2>
                <div>
                  <!--                  <el-button type="danger" @click="userAllClear">重置</el-button>-->
                  <el-button type="info" @click="getUser" icon="el-icon-refresh">刷新</el-button>
                  <el-button type="primary" @click="addUser" icon="el-icon-plus">新增</el-button>
                </div>
              </div>
              <el-table :data="userList" style="width: 100%" v-loading="isUsersLoading">
                <el-table-column prop="id" label="序号"></el-table-column>
                <el-table-column
                    prop="username"
                    label="用户名"
                ></el-table-column>
                <el-table-column
                    prop="permission_level"
                    label="权限级别"
                ></el-table-column>
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <el-button
                        @click="editUser(scope.$index, scope.row)"
                        type="success"
                    >修改
                    </el-button
                    >
                    <el-button
                        @click="confirmDeleteUser(scope.row)"
                        type="danger"
                    >删除
                    </el-button
                    >
                  </template>
                </el-table-column>
              </el-table>
              <el-pagination
                  @size-change="handleSizeChangeUser"
                  @current-change="handleCurrentChangeUser"
                  :current-page="currentPageUser"
                  :page-sizes="[5, 10, 20, 50]"
                  :page-size="pageSizeUser"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="totalUsers">
              </el-pagination>
            </el-card>
          </el-col>

          <!-- 指令列表 -->
          <el-col title="指令列表" :span="12">
            <el-card>
              <div
                  style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                "
              >
                <h2 style="flex-grow: 0; text-align: center; margin: 0">
                  指令列表</h2>
                <div>
                  <!--                  <el-button type="danger" @click="deleteUser">重置</el-button>-->
                  <el-button type="info" @click="getCommand" icon="el-icon-refresh">刷新</el-button>
                  <el-button type="primary" @click="addCommand" icon="el-icon-plus">新增</el-button>
                </div>
              </div>
              <el-table :data="commandList" style="width: 100%" v-loading="isCommandLoading">
                <el-table-column prop="action" label="指令"></el-table-column>
                <el-table-column prop="level" label="权限等级"></el-table-column>
                <el-table-column prop="label" label="标签"></el-table-column>
                <!--                <el-table-column prop="slot" label="槽位列表"></el-table-column>-->
                <el-table-column label="操作">
                  <template slot-scope="scope">
                    <!-- 新增“修改”按钮 -->
                    <el-button type="success" @click="editCommand(scope.row)">修改</el-button>
                    <el-button type="danger" @click="confirmDeleteCommand(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-pagination
                  @size-change="handleSizeChangeCommand"
                  @current-change="handleCurrentChangeCommand"
                  :current-page="currentPageCommand"
                  :page-sizes="[5, 10, 20, 50]"
                  :page-size="pageSizeCommand"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="totalCommands">
              </el-pagination>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <!-- 用户表单对话框 -->
    <el-dialog
        :title="dialogTitle"
        :visible.sync="userDialogFormVisible"
        width="40%"
    >
      <el-form :model="userFormData" ref="form" v-loading="isUploading" element-loading-text="正在提交">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="userFormData.username"></el-input>
        </el-form-item>
        <el-form-item label="等级" :label-width="formLabelWidth">
          <el-input
              v-model="userFormData.permission_level"
              type="number"
          ></el-input>
        </el-form-item>
        <el-form-item label="音频文件" :label-width="formLabelWidth">
          <el-upload
              class="upload-demo"
              drag
              action="#"
              :auto-upload="false"
              :multiple="true"
              :before-upload="handleBeforeUpload"
              :on-change="handleFileChange"
              :file-list="fileList"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div class="el-upload__tip" slot="tip">只能上传wav文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <ul>
            <li v-for="(file, index) in fileList" :key="index">
              <i class="el-icon-document"></i> {{ file.name }}
            </li>
          </ul>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="userDialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>


    <el-dialog
        title="修改用户信息"
        :visible.sync="userEditDialogFormVisible"
        width="40%"
    >
      <el-form :model="userFormData" ref="form" v-loading="isUploading" element-loading-text="正在提交">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <el-input v-model="userFormData.username"></el-input>
        </el-form-item>
        <el-form-item label="等级" :label-width="formLabelWidth">
          <el-input
              v-model="userFormData.permission_level"
              type="number"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="userEditDialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>

    <!-- 音频识别对话框 -->
    <el-dialog
        title="音频识别"
        :visible.sync="audioDialogFormVisible"
        width="50%"
    >
      <el-form :model="userFormData" ref="form" v-loading="isRecognizing" element-loading-text="正在识别">
        <el-form-item label="音频文件" :label-width="formLabelWidth">
          <el-upload
              class="upload-demo"
              drag
              action="#"
              :auto-upload="false"
              :multiple="true"
              :before-upload="handleBeforeUpload"
              :on-change="handleFileChange"
              :file-list="fileList"
              :limit="1"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div class="el-upload__tip" slot="tip">只能上传wav文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <ul>
            <li v-for="(file, index) in fileList" :key="index">
              <i class="el-icon-document"></i> {{ file.name }}
            </li>
          </ul>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="audioDialogFormVisible = false" :disabled="isRecognizing">取消</el-button>
        <el-button type="primary" @click="recognizeAudio" :disabled="isRecognizing">确定</el-button>
      </div>
    </el-dialog>
    <!-- 声纹识别对话框 -->
    <el-dialog
        title="声纹识别"
        :visible.sync="audioPrintDialogFormVisible"
        width="40%"
    >
      <el-form :model="userFormData" ref="form" v-loading="isRecognizingVoicePrint" element-loading-text="正在识别">
        <el-form-item label="音频文件" :label-width="formLabelWidth">
          <el-upload
              class="upload-demo"
              drag
              action="#"
              :auto-upload="false"
              :multiple="true"
              :before-upload="handleBeforeUpload"
              :on-change="handleFileChange"
              :file-list="fileList"
              :limit="1"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div class="el-upload__tip" slot="tip">只能上传wav文件</div>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <ul>
            <li v-for="(file, index) in fileList" :key="index">
              <i class="el-icon-document"></i> {{ file.name }}
            </li>
          </ul>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="audioDialogFormVisible = false" :disabled="isRecognizingVoicePrint">取消</el-button>
        <el-button type="primary" @click="recognize" :disabled="isRecognizingVoicePrint">确定</el-button>
      </div>
    </el-dialog>
    <!-- 录音页面对话框 -->
    <el-dialog
        title="开始录音"
        :visible.sync="isRecordingPage"
        width="50%"
    >
      <el-form :model="userFormData" ref="form" v-loading="isUploading">
        <el-form-item label="请说出唤醒语句：" :label-width="formLabelWidth">
          <h2>{{ randomNumber }}</h2>
        </el-form-item>
        <el-form-item>
          <el-button
              v-if="!isRecording"
              type="primary"
              @click="startRecording"
          >开始录音
          </el-button
          >
          <el-button
              v-if="isRecording"
              type="danger"
              @click="stopRecording"
          >结束录音
          </el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
    <!-- 指令表单对话框（新增） -->
    <el-dialog
        :title="commandDialogTitle"
        :visible.sync="commandDialogFormVisible"
        width="30%"
    >
      <el-form :model="commandFormData" ref="commandForm" :label-width="formLabelWidth">
        <el-form-item label="指令名称">
          <el-input v-model="commandFormData.action"></el-input>
        </el-form-item>
        <el-form-item label="权限等级">
          <el-input v-model="commandFormData.level" type="number"></el-input>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="commandFormData.label"></el-input>
        </el-form-item>
        <el-form-item label="槽位列表">
          <el-input v-model="commandFormData.slot"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="commandDialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCommandForm">确定</el-button>
      </div>
    </el-dialog>
    <!-- ...模板结束 -->

  </div>
</template>

<script>
import axios from "axios";
import toWav from 'audiobuffer-to-wav';


export default {
  data() {
    return {
      httpTarget: "http://127.0.0.1:5000", // 定义全局 HTTP 目标
      info: "",
      userList: [], // 初始化为空
      commandList: [], // 初始化为空
      currentPageUser: 1, // 用户表格的当前页
      currentPageCommand: 1, // 指令表格的当前页
      pageSizeUser: 5, // 用户表格的每页显示数量
      pageSizeCommand: 5, // 指令表格的每页显示数量
      totalUsers: 0, // 用户总数
      totalCommands: 0, // 指令总数
      userDialogFormVisible: false,
      userEditDialogFormVisible: false,
      audioDialogFormVisible: false,
      audioPrintDialogFormVisible: false,
      shouldRegenerate: false,
      formLabelWidth: "200px",
      userFormData: {
        username: "",
        permission_level: 1,
        user_id: 0,
      },
      dialogTitle: "新增用户",
      isEditing: false,
      fileList: [],
      isRecognizing: false, // 增加识别状态
      isRecognizingVoicePrint: false, // 增加识别状态
      isWake: true,
      // TODO 调试TRUE
      isUploading: false,
      isCommandLoading: false,
      isUsersLoading: false,
      isRecordingPage: false,    // 控制是否为录音页面
      isRecording: false,        // 是否正在录音
      randomNumber: "",          // 显示的随机数字
      audioUrl: "",              // 录音完成后的音频文件 URL
      mediaRecorder: null,       // 录音实例
      audioChunks: [],           // 录音数据
      audioBlob: null,           // 录音的 Blob 对象
      wavFile: null,          // 录音的wav文件
      /* -------- Command Dialog 相关新增 -------- */
      commandDialogFormVisible: false,
      commandDialogTitle: "新增指令",
      isCommandEditing: false,
      commandFormData: {
        id: 0,
        action: "指令名称",
        level: 1,
        label: "LAUNCH",
        slot: ""
      },
    };
  },
  mounted() {
    // 页面加载时请求指令列表
    this.getCommand();
    this.getUser();
  },
  methods: {
    // 识别按钮
    recognize() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      this.fileList = [];
      this.audioDialogFormVisible = true;
    },

    recognizeAudioprint() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      this.fileList = [];
      this.audioPrintDialogFormVisible = true;
    },

    // 识别音频
    async recognizeAudio() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      console.log("recognizeAudio");
      console.log("file length: " + this.fileList.length);
      this.isRecognizing = true; // 开始识别，设置加载状态
      let formData = new FormData();
      formData.append(`audio_file1`, this.fileList[0].raw);
      // this.fileList.forEach((file, index) => {
      //   formData.append(`audio_file${index + 1}`, file.raw);
      // });
      axios
          .post(`${this.httpTarget}/recognize`, formData)
          .then((response) => {
            if (response.data.result === "Success") {
              console.log(response)
              if (response.data.data.possible_action === "No matching actions found")
              this.info = `识别的指令为：${response.data.data.possible_action}
                识别的用户为：${response.data.data.username}(${response.data.data.user_id})
                权限等级为： ${response.data.data.permission_level}`;
            } else if (response.data.result === "Failed" && response.data.error !== undefined) {
              this.$message.error(
                  `识别失败：未找到足够相似度的对象`
              );
              this.info = `识别失败：未找到足够相似度的对象,最大相似度为 ${response.data.data.similarity_score}`
            } else {
              this.$message.error(`发生错误: ${response.data.data.error}`);
            }
            this.audioDialogFormVisible = false;
            this.fileList = [];
          })
          .catch((error) => {
            this.$message.error(`识别失败: ${error.message}`);
          })
          .finally(() => {
            this.isRecognizing = false; // 识别结束，取消加载状态
          });
    },
    // 识别声纹
    async recognizeVoicePrint() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      console.log("recognizeVoicePrint");
      console.log("file length: " + this.fileList.length);
      this.isRecognizingVoicePrint = true; // 开始识别，设置加载状态
      let formData = new FormData();
      formData.append(`audio_file1`, this.fileList[0].raw);
      try {
        const response = await axios.post(`${this.httpTarget}/recognizeAudioPrint`, formData);
        if (response.data.result === "Success") {
          console.log(response);
          this.info = `
            识别的用户为：${response.data.data.user_name}(${response.data.data.user_id})`;
        } else if (response.data.result === "Failed" && response.data.error !== undefined) {
          this.$message.error(
              `识别失败：未找到足够相似度的声纹`
          );
          this.info = `识别失败：未找到足够相似度的声纹, 最大相似度为 ${response.data.data.similarity_score}`;
        } else {
          console.log(response)
          this.$message.error(`发生错误: ${response.data.data.error}`);
        }
        this.audioDialogFormVisible = false;
        this.fileList = [];
      } catch (error) {
        console.log(error)
        this.$message.error(`识别失败: ${error.message}`);
      } finally {
        this.isRecognizingVoicePrint = false; // 识别结束，取消加载状态
      }
    },

    // 跳转到录音页面
    goToRecordingPage() {
      this.isRecordingPage = true;
      this.generateRandomNumber();  // 生成随机数字
    },

    // 生成随机数字
    generateRandomNumber() {
      const chineseNumbers = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'];
      const length = Math.floor(Math.random() * 6) + 10; // 10-15位
      let result = '';

      for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * 10); // 0-9
        result += chineseNumbers[randomIndex];
      }

      this.randomNumber = result;
      console.log(this.randomNumber);
      return result;
    },

    async startRecording() {
      try {
        this._resetRecordingState();
        this.info = "初始化麦克风...";

        const stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            sampleRate: 16000,
          },
          video: false
        });

        this._initMediaRecorder(stream);
        this.mediaRecorder.start(500); // 500ms数据切片
        this.isRecording = true;
        this.info = "录音进行中... 🔊";
      } catch (err) {
        this._handleRecordingError(err);
      }
    },

    // 停止录音
    stopRecording() {
      if (!this.mediaRecorder || this.mediaRecorder.state === 'inactive') return;

      try {
        this.mediaRecorder.stop();
        this.isRecording = false;
        this.info = "正在处理音频...";

        this.mediaRecorder.stream.getTracks().forEach(track => {
          track.stop();
          track.enabled = false;
        });

      } catch (error) {
        console.error("停止录音失败:", error);
        this.$message.error("停止录音时发生错误");
      }
    },

    // 内部方法：初始化录音器
    _initMediaRecorder(stream) {
      const mimeType = this._getSupportedMimeType();
      this.mediaRecorder = new MediaRecorder(stream, {
        mimeType,
        audioBitsPerSecond: 16000
      });

      // 数据收集
      this.mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) this.audioChunks.push(e.data);
      };

      // 录音结束处理
      this.mediaRecorder.onstop = async () => {
        try {
          const originalBlob = new Blob(this.audioChunks, {type: this.mediaRecorder.mimeType});
          this.audioBlob = await this._convertToWav(originalBlob);
          this.audioUrl = URL.createObjectURL(this.audioBlob);
          this.$nextTick(this.wake);
        } catch (error) {
          console.error("音频处理失败:", error);
          this.$message.error("音频格式转换失败");
        } finally {
          this.isRecordingPage = false;
        }
      };

      // 错误处理
      this.mediaRecorder.onerror = (e) => {
        console.error("录音器错误:", e);
        this.$message.error("录音设备异常");
        this.stopRecording();
      };
    },

    // 格式转换
    async _convertToWav(blob) {
      const audioContext = new AudioContext({sampleRate: 16000});
      try {
        const buffer = await blob.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(buffer);

        const wavBuffer = toWav(audioBuffer, {
          sampleRate: 16000,
          channelCount: 1,
          bitDepth: 16
        });
        this.wavFile = new File([wavBuffer], `wake_${Date.now()}.wav`, {type: 'audio/wav'});
        return new Blob([wavBuffer], {type: 'audio/wav'});
      } finally {
        audioContext.close();
      }
    },

    // 获取支持的MIME类型
    _getSupportedMimeType() {
      const candidates = [
        'audio/webm;codecs=opus',
        'audio/ogg;codecs=opus',
        'audio/mp4',
        'audio/x-m4a'
      ];
      return candidates.find(MediaRecorder.isTypeSupported.bind(MediaRecorder));
    },

    // 重置录音状态
    _resetRecordingState() {
      this.audioChunks = [];
      this.audioBlob = null;
      if (this.audioUrl) URL.revokeObjectURL(this.audioUrl);
      this.audioUrl = '';
      this.info = "";
    },

    // 错误处理
    _handleRecordingError(err) {
      console.error("录音初始化失败:", err);
      this.$message.error({
        content: `麦克风访问被拒绝: ${err.message}`,
        duration: 3000
      });
      this.isRecording = false;
      this.isRecordingPage = false;
    },


    async wake() {
      try {
        this.isUploading = true;

        // 构建符合API文档要求的表单数据
        const formData = new FormData();
        formData.append('file', this.wavFile); // 根据文档字段要求
        formData.append('wake_text', this.randomNumber.toString());

        // 发送请求
        const {data} = await axios.post(`${this.httpTarget}/wake`, formData);

        // 处理响应
        if (data.result === 'Success') {
          this.handleWakeSuccess(data.data);
        } else if (data.result === 'Failed') {
          this.handleWakeFailure(data.data?.error);
        } else {
          console.log(data)
          this.$message.error('无效的响应格式');
        }

      } catch (error) {
        this.handleNetworkError(error);
      } finally {
        this.cleanup();
      }
    },

// 唤醒成功处理
    handleWakeSuccess(responseData) {
      this.$message.success({
        message: `身份验证成功，欢迎用户 ${responseData.user_name}`,
        description: `识别内容："${responseData.recognized_text}"`,
        duration: 5000
      });

      this.isWake = true;
      this.currentUser = {
        id: responseData.user_name,
        lastRecognized: responseData.recognized_text
      };

      this.$emit('wake-success', {
        userId: responseData.user_name,
        timestamp: new Date().toISOString()
      });
    },

// 唤醒失败处理
    handleWakeFailure(errorMessage) {
      const errorActions = {
        '声纹精度不够': {
          message: '匹配程度不够,请重试',
          action: () => this.generateNewVerificationCode()
        },
        '文本不匹配': {
          message: '验证码错误',
          action: () => this.generateNewVerificationCode()
        },
        '未找到对应用户': {
          message: '请注册用户',
          action: () => this.generateNewVerificationCode()
        }
      };

      const matchedError = Object.entries(errorActions).find(
          ([key]) => errorMessage.includes(key)
      );

      if (matchedError) {
        const {message, action} = matchedError[1];
        this.$message({
          type: 'error',
          message: message,
          duration: 2000,
          onClose: () => {
            action(); // 在错误提示关闭后执行
          }
        });
      } else {
        this.$message.error(errorMessage || '未知错误');
      }
    },

// 生成新验证码
    generateNewVerificationCode() {
      this.generateRandomNumber();
      this.$message.info(`新验证码已生成：${this.randomNumber}`);
    },


// 网络错误处理
    handleNetworkError(error) {
      const status = error.response?.status;
      let message = '请求失败：';

      switch (status) {
        case 400:
          message += '请求参数错误';
          break;
        case 413:
          message += '音频文件大小超过限制';
          break;
        case 415:
          message += '不支持的音频格式';
          break;
        case 500:
          message += '服务器内部错误';
          break;
        default:
          message += error.message || '网络连接异常';
      }

      this.$message.error(message);
    },

// 清理资源
    cleanup() {
      this.isUploading = false;
      this.audioDialogFormVisible = false;
      this._resetRecordingState();

    },

    // 添加用户
    addUser() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      this.dialogTitle = "新增用户";
      this.isEditing = false;
      this.userFormData = {
        username: "",
        permission_level: 1,
      };
      this.fileList = [];
      this.userDialogFormVisible = true;
    },

    // 编辑用户
    editUser(index, row) {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      this.dialogTitle = "修改用户";
      this.isEditing = true;
      this.userFormData = {
        username: row.username,
        permission_level: row.permission_level,
        user_id: row.id,
      };
      this.userEditDialogFormVisible = true;
    },

    // 在上传文件之前检查文件格式
    handleBeforeUpload(file) {
      const isWav = file.type === "audio/wav";
      if (!isWav) {
        this.$message.error("只能上传wav格式的文件");
      }
      return isWav;
    },

    // 处理文件上传
    handleFileChange(file, fileList) {
      this.fileList = fileList;
    },

    // 提交表单
    async submitForm() {
      this.isUploading = true;
      if (
          !this.userFormData.username ||
          !this.userFormData.permission_level ||
          (!this.isEditing && this.fileList.length === 0)
      ) {
        this.isUploading = false;
        this.$message.error(
            "请填写完整信息，包括用户名、等级和至少一个音频文件"
        );
        return;
      }

      const formData = new FormData();
      formData.append("username", this.userFormData.username);
      formData.append("permission_level", this.userFormData.permission_level);
      if (this.isEditing) {
        formData.append("id", this.userFormData.user_id);
      }
      this.fileList.forEach((file, index) => {
        formData.append(`audio_file${index + 1}`, file.raw);
      });

      try {
        if (this.isEditing) {
          console.log(
              this.userFormData.username +
              " " +
              this.userFormData.permission_level +
              " " +
              this.userFormData.user_id
          );
          axios
              .post(`${this.httpTarget}/update_user`, formData)
              .then((response) => {
                if (response.data.result === "Success") {
                  this.$message.success(`用户修改成功`);
                  this.getUser();
                } else {
                  this.$message.error(`修改失败: ${response.data.result}`);
                }
              })
              .catch((error) => {
                this.$message.error(`修改失败: ${error.message}`);
              })
              .finally(() => {
                this.isUploading = false;
              });
        } else {
          axios
              .put(`${this.httpTarget}/load`, formData)
              .then((response) => {
                if (response.data.result === "Success") {
                  this.$message.success(`用户新增成功`);
                  this.getUser();
                } else {
                  this.$message.error(`新增失败: ${response.data.data.error}`);
                }
              })
              .catch((error) => {
                this.$message.error(`新增失败: ${error.message}`);
              })
              .finally(() => {
                this.isUploading = false;
              });
        }
        // const url = this.isEditing
        //   ? `${this.httpTarget}/update_user`
        //   : `${this.httpTarget}/load`;
        // const response = await axios.put(url, formData, {
        //   headers: {
        //     "Content-Type": "multipart/form-data",
        //   },
        // });

        this.userDialogFormVisible = false;
        this.fileList = [];
        this.userFormData = {
          username: "",
          permission_level: 1,
        };
        this.getUser();
      } catch (error) {
        console.error("提交表单出错:", error);
      }
    },

    // 获取用户数据
    getUser() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      this.isUsersLoading = true
      axios.get(`${this.httpTarget}/get_all_user`).then((response) => {
        if (response.data.result === "Success") {
          const users = response.data.data.user_set.map((user) => ({
            username: user.username,
            permission_level: user.permission_level,
            id: user.id,
          }));
          this.totalUsers = users.length;
          this.userList = users.slice(
              (this.currentPageUser - 1) * this.pageSizeUser,
              this.currentPageUser * this.pageSizeUser
          );
        } else {
          this.$message.error(`获取用户列表失败: ${response.data.data.error}`);
        }
      }).catch((error) => {
        this.$message.error(`请求用户列表失败: ${error.message}`);
      })
          .finally(() => {
            this.isUsersLoading = false;
          });
    },

    // 删除确认
    confirmDeleteUser(row) {
      this.$confirm(
          `确定要删除用户 "${row.username}(id=${row.id})" 吗?`,
          "确认删除",
          {
            confirmButtonText: "确认",
            cancelButtonText: "取消",
            type: "warning",
          }
      )
          .then(() => {
            // 调用删除函数
            this.deleteUser(row);
          })
          .catch(() => {
            this.$message.info("已取消删除");
          });
    },

    // 删除指令
    deleteUser(row) {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      let formData = new FormData();
      formData.append("user_id", row.id);
      axios
          .post(`${this.httpTarget}/delete_user`, formData)
          .then((response) => {
            if (response.data.result === "Success") {
              this.$message.success(`用户 "${row.username}" 删除成功`);
              this.getUser();
            } else {
              this.$message.error(`删除失败: ${response.data.data.error}`);
            }
          })
          .catch((error) => {
            this.$message.error(`删除失败: ${error.message}`);
          });
    },

    userAllClear() {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      this.isUploading = true
      axios
          .get(`${this.httpTarget}/delete_all_user`,)
          .then((response) => {
            if (response.data.result === "Success") {
              this.$message.success("执行成功")
            } else if (response.data.result === "Failed") {
              this.$message.error("执行失败")
            } else {
              this.$message.error("执行错误")
            }
          })
          .catch((e) => {
            this.$message.error(`执行错误${e.message}`);
          })
          .finally(() => {
            this.getUser()
            this.isUploading = false;
          })
    },
    /* --- 指令表单逻辑新增/修改开始 --- */
    addCommand() {
      if (!this.isWake) return this.$message.warning('请先唤醒系统');
      this.commandDialogTitle = "新增指令";
      this.isCommandEditing = false;
      this.commandFormData = {id: 0, action: "", level: 1, label: "LAUNCH", slot: ""};
      this.commandDialogFormVisible = true;
    },
    editCommand(row) {
      if (!this.isWake) return this.$message.warning('请先唤醒系统');
      this.commandDialogTitle = "修改指令";
      this.isCommandEditing = true;
      this.commandFormData = {...row};          // 直接复制行数据
      this.commandDialogFormVisible = true;
    },
    async submitCommandForm() {
      this.isUploading = true;
      const fd = new FormData();
      Object.entries(this.commandFormData).forEach(([k, v]) => fd.append(k, v));
      try {
        if (this.isCommandEditing) {
          await axios.post(`${this.httpTarget}/update_action`, fd);
          this.$message.success("指令修改成功");
        } else {
          await axios.post(`${this.httpTarget}/add_action`, fd);
          this.$message.success("指令新增成功");
        }
        this.getCommand();
        this.commandDialogFormVisible = false;
      } catch (e) {
        this.$message.error(`操作失败: ${e.message}`);
      } finally {
        this.isUploading = false;
      }
    },
    /* --- 指令表单逻辑新增/修改结束 --- */

    // 删除确认
    confirmDeleteCommand(row) {
      this.$confirm(`确定要删除指令 "${row.command}" 吗?`, "确认删除", {
        confirmButtonText: "确认",
        cancelButtonText: "取消",
        type: "warning",
      })
          .then(() => {
            // 调用删除函数
            this.deleteCommand(row);
          })
          .catch(() => {
            this.$message.info("已取消删除");
          });
    },


    getCommand() {
      if (!this.isWake) return this.$message.warning('请先唤醒系统');
      this.isCommandLoading = true;
      axios.get(`${this.httpTarget}/get_all_action`)
          .then(res => {
            if (res.data.result === "Success") {
              console.log(res.data.data.action_set)
              const cmds = res.data.data.action_set.map(c => ({
                id: c.id,
                action: c.action,
                level: c.level,
                label: c.label,
                slot: c.slot,
              }));
              this.totalCommands = cmds.length;
              this.commandList = cmds.slice(
                  (this.currentPageCommand - 1) * this.pageSizeCommand,
                  this.currentPageCommand * this.pageSizeCommand
              );
            } else {
              this.$message.error(`获取指令失败: ${res.data.data.error}`);
            }
          })
          .catch(e => this.$message.error(`请求指令列表失败: ${e.message}`))
          .finally(() => this.isCommandLoading = false);
    },

    // 删除指令
    deleteCommand(row) {
      // 检查isWake字段的值
      if (!this.isWake) {
        // 如果isWake为false，弹出提示并终止函数执行
        this.$message.warning('请先唤醒系统');
        return; // 使用return终止函数的进一步执行
      }
      let formData = new FormData();
      formData.append("action", row.action);
      // formData.append("id", row.id);
      axios
          .post(`${this.httpTarget}/delete_action`, formData)
          .then((response) => {
            if (response.data.result === "Success") {
              this.$message.success(`指令 "${row.command}" 删除成功`);
              this.getCommand();
            } else {
              this.$message.error(`删除失败: ${response.data.data.error}`);
            }
          })
          .catch((error) => {
            this.$message.error(`删除失败: ${error.message}`);
          });
    },
    // 分页大小改变时的处理（用户表格）
    handleSizeChangeUser(size) {
      this.pageSizeUser = size;
      this.getUser();
    },

    // 分页大小改变时的处理（指令表格）
    handleSizeChangeCommand(size) {
      this.pageSizeCommand = size;
      this.getCommand();
    },

    // 当前页码改变时的处理（用户表格）
    handleCurrentChangeUser(page) {
      this.currentPageUser = page;
      this.getUser();
    },

    // 当前页码改变时的处理（指令表格）
    handleCurrentChangeCommand(page) {
      this.currentPageCommand = page;
      this.getCommand();
    },
  },
};
</script>
