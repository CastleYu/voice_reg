FROM python:3.10.5
LABEL authors="casyu"



# pip 阿里云镜像
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
# 设置镜像源不验证 SSL
ENV PIP_TRUSTED_HOST=mirrors.aliyun.com

# 工作目录
RUN mkdir /app
WORKDIR /app

# 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码到容器中
COPY . .

# 暴露 Flask 应用运行的端口（假设为 5000）
EXPOSE 5000

# 设置必要的环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py", "--host=0.0.0.0"]