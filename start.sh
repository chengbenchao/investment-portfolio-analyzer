#!/bin/bash
# 标准启动入口：A股投资组合分析系统
set -e

cd "$(dirname "$0")"

PYTHON="python3"
if [ -x ".venv/bin/python" ]; then
    VENV_PY="$(pwd)/.venv/bin/python"
    if "$VENV_PY" -c "import flask, flask_cors, requests" >/dev/null 2>&1; then
        echo "✅ 使用项目虚拟环境 .venv"
        PYTHON="$VENV_PY"
    else
        echo "⚠️ .venv 存在但依赖不完整，回退到系统 Python"
    fi
else
    echo "⚠️ 未找到 .venv，回退到系统 Python"
fi

# 启动前自检
./selfcheck.sh

echo "🚀 启动 A股投资组合分析系统..."
echo "🌐 本机访问: http://127.0.0.1:8002"
echo "📘 API 示例: http://127.0.0.1:8002/api/search?keyword=招商银行"
echo "🛑 停止服务: Ctrl+C"
echo ""

exec "$PYTHON" main.py
