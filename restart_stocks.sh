#!/bin/bash
# 重新配置A股投资组合到8000端口

echo "=" 
echo "🔄 重新配置A股投资组合"
echo "=" 

# 停止旧进程
echo ""
echo "🧹 清理旧进程..."
pkill -f "cloudflare" 2>/dev/null
pkill -f "python3.*http.server" 2>/dev/null
pkill -f "python.*investment" 2>/dev/null
sleep 2

# 切换到项目目录
cd /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio || exit 1

# 启动Python HTTP服务器
echo ""
echo "🚀 启动A股投资组合（8000端口）..."
python3 -m http.server 8000 &
sleep 2

echo ""
echo "=" 
echo "✅ 本地服务已启动"
echo "=" 
echo ""
echo "📍 本地访问: http://localhost:8000"
echo ""
echo "🌐 需要启动Cloudflare Tunnel才能公网访问"
echo "💡 Tunnel地址每次启动都会变化"
echo ""
echo "=" 
echo "📊 项目信息"
echo "=" 
echo ""
echo "📁 位置: /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio"
echo "🔢 端口: 8000"
echo "📝 功能: A股投资组合分析"
echo ""
echo "=" 
echo "💡 下一步"
echo "=" 
echo ""
echo "现在请告诉我："
echo "1️⃣ 需要我启动Cloudflare Tunnel吗？"
echo "2️⃣ 还是你本地访问就够了？"
echo ""
echo "如果需要Tunnel，我会给你新的trycloudflare.com地址！"
echo ""
echo "="
