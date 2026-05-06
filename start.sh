#!/bin/bash
# 启动投资组合后端服务

cd "$(dirname "$0")"

# 激活虚拟环境
if [ -d "venv" ]; then
    echo "✅ 使用虚拟环境..."
    source venv/bin/activate
else
    echo "⚠️ 虚拟环境未找到，使用系统Python..."
fi

# 检查依赖
python3 -c "import flask; import flask_cors; import requests" 2>/dev/null || {
    echo "📦 安装依赖..."
    pip install -q flask flask-cors requests
}

# 启动服务
echo "🚀 启动投资组合服务..."
echo "📱 访问地址: http://localhost:8002"
echo "🔧 停止服务: Ctrl+C"
echo ""

python3 app.py
