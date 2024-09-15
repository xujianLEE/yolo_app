# 使用官方Python基础镜像
FROM python:3.9-slim

# 安装OpenCV所需的库
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用运行的端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py

# 启动Flask应用
CMD ["flask", "run", "--host=0.0.0.0"]