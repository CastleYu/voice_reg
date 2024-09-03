# 声纹/指令识别

- 前端
  1. https://gitee.com/gailingtuo/speech_frontend
  2. https://gitee.com/muziyuc/SpeechSimpleFrontend
- 后端
  1. https://github.com/tttungwu/Speech
  2. https://gitee.com/muziyuc/VoiceprintRecognition


## build

### 创建conda环境

```sh
conda create --name speech python=3.8
```

### 安装必要的包
请**有序**完成下列安装
(出现 `paddlespeech` 需要 `librosa==0.8.1` 警告属于正常现象)
```shell
pip install paddlepaddle==2.4.1 pytest-runner  -i https://pypi.tuna.tsinghua.edu.cn/simple
```
```shell
pip install librosa==0.10.1 pymilvus pymysql transformers sentence_transformers LAC pydub noisereduce flask_cors sqlalchemy -i https://pypi.tuna.tsinghua.edu.cn/simple
```
```shell
pip install pytest-runner -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install paddlespeech==1.4.1 -i https://pypi.tuna.tsinghua.edu.cn/simple

```

[//]: # (```shell)

[//]: # (pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple)

[//]: # (```)
#### pytorch
- Windows:
```sh
pip install torch
pip install torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- Linux:
```sh
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 数据库配置（已部署服务器可忽略）

- 在`config.yaml`下配置内容

#### mysql

- 启动
- `.\data`目录在仓库中的`database\mysql`目录下，可以根据需要挂载到你自己的地址

```shell
cd database\mysql
```

```sh
docker run --privileged=true  -v .\data\:/var/lib/mysql -v .\logs\:/var/log/mysql -v .\conf\:/etc/mysql -v .\my.cnf:/etc/mysql/my.cnf  -p 8886:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql
```

- 可视化：Navicat等工具

#### milvus

- 启动
    - 首先切换到目录`Speech\database\milvus`下，可以看到一个docker-compose.yml文件，`docker compose up -d`即可

```shell
cd Speech\database\milvus
```

```
docker compose up -d
```

- 可视化：https://github.com/zilliztech/attu
