FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY src/ ./src/
COPY index.html .

# 创建日志目录
RUN mkdir -p logs

EXPOSE 8002

CMD ["python", "main.py"]
