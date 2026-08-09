import logging
import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from service.device import function_list
from xf.config import STTConfig as cfg
from xf.llm import XFSparkAI
from xf.stt import XFYunSTT

app = Flask(__name__)
CORS(app)  # 启用全局 CORS

stt = XFYunSTT(cfg.APP_ID, cfg.API_KEY, cfg.API_SECRET)
llm = XFSparkAI().load_function(function_list)


@app.route('/stt', methods=['POST'])
def speech_to_text():
    """
    接收语音文件，返回文字结果
    请求格式：
    表单数据，包含文件字段 "file"
    """
    try:
        logging.info("接受文件")
        if 'file' not in request.files:
            return jsonify({
                "error": "No file uploaded"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "error": "Empty file uploaded"}), 400

        # 将文件保存到临时路径
        logging.info("保存文件")
        temp_path = os.path.join(".", "tmp", file.filename)
        file.save(temp_path)

        # 调用语音转文字模块
        result = stt.read_file(temp_path)
        os.remove(temp_path)  # 删除临时文件
        print(result)
        return jsonify({
            "text": result}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"{type(e)}{str(e)}"}), 501


@app.route('/parse_command', methods=['POST'])
def parse_command():
    """
    接收文本指令，返回解析后的结果
    请求格式：
    {
        "command": "打开主卧空调"
    }
    """
    try:
        data = request.get_json()
        command = data.get('command')

        if not command:
            return jsonify({
                "error": "No command provided"}), 400

        # 调用文字指令解析模块
        result = llm.send(command)
        return jsonify({
            "parsed_command": result}), 200
    except Exception as e:
        return jsonify({
            "error": str(e)}), 500


@app.route('/execute', methods=['POST'])
def execute():
    """
    接收解析后的指令并执行相应动作
    请求格式：
    {
        "name": "控制空调",
        "arguments": {
            "action": "turn_on",
            "location": "主卧"
        }
    }
    """
    try:
        data = request.get_json()
        name = data.get('name')
        arguments = data.get('arguments')

        if not name or not arguments:
            return jsonify({
                "error": "Invalid input"}), 400

        # 假设这里直接返回成功信息，实际可根据需求执行设备控制逻辑
        return jsonify({
            "status": "success",
            "executed_command": name,
            "arguments": arguments}), 200
    except Exception as e:
        return jsonify({
            "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
