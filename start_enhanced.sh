#!/bin/bash

# A股投资分析助手 - 增强版启动脚本
# 集成阿里云百炼AI分析

echo "="*80
echo "🚀 A股投资分析助手 - 增强版"
echo "="*80
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装依赖..."
pip install -q flask flask-cors requests

echo ""
echo "="*80
echo "🔑 配置说明"
echo "="*80
echo "请确保已设置阿里云百炼API密钥："
echo "  export BAILIAN_API_KEY='你的API密钥"
echo ""
echo "如果没有API密钥，请先在阿里云百炼平台申请："
echo "  https://bailian.console.aliyun.com/"
echo ""

# 检查API密钥
if [ -z "$BAILIAN_API_KEY" ]; then
    echo "⚠️  警告：未设置 BAILIAN_API_KEY 环境变量"
    echo "   AI分析功能将无法使用"
    echo ""
    read -p "是否继续启动？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ BAILIAN_API_KEY 已设置"
fi

echo ""
echo "="*80
echo "🌐 启动服务"
echo "="*80
echo "📊 本地访问: http://localhost:8002"
echo "📄 报告目录: $(pwd)/reports"
echo ""
echo "按 Ctrl+C 停止服务"
echo "="*80
echo ""

# 启动增强版应用
python3 enhanced_app.py
