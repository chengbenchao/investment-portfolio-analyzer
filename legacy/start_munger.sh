#!/bin/bash
# 历史变体脚本：功能与 ./start.sh 重叠，不是标准入口

# 芒格智慧版 - A股投资组合分析系统启动脚本

echo "========================================="
echo "  🧠 芒格智慧 - A股投资组合分析系统"
echo "========================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3"
    exit 1
fi

echo "🚀 启动服务中..."
echo "📍 访问地址: http://localhost:8002"
echo "🔧 经典版地址: http://localhost:8002/classic"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""
echo "========================================="
echo ""

cd "$(dirname "$0")"
python3 main.py
