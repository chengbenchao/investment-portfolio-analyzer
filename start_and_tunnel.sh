#!/bin/bash
# 启动A股投资组合的Cloudflare Tunnel

echo "=" 
echo "🚀 启动A股投资组合和Cloudflare Tunnel"
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

# 尝试启动Cloudflare Tunnel
echo ""
echo "🌐 尝试启动Cloudflare Tunnel..."
echo ""
echo "=" 
echo "📊 服务状态"
echo "=" 
echo ""
echo "📍 本地访问: http://localhost:8000"
echo ""
echo "=" 
echo "💡 重要提示"
echo "=" 
echo ""
echo "🌐 Cloudflare Tunnel需要单独启动"
echo "🔄 每次启动Tunnel都会生成新的地址"
echo "📝 你可以用cloudflared命令自己启动Tunnel"
echo ""
echo "=" 
echo "🎯 给你的方案"
echo "=" 
echo ""
echo "方案1️⃣：我帮你启动Tunnel（会生成新地址）"
echo "方案2️⃣：你本地用 http://localhost:8000 就够了"
echo ""
echo "请告诉我你想要哪个？"
echo ""
echo "="
