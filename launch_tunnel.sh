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

# 启动Cloudflare Tunnel
echo ""
echo "🌐 启动Cloudflare Tunnel..."
echo ""
echo "⏳ Tunnel正在启动，请稍等..."
echo ""

# 启动cloudflared tunnel
cloudflared tunnel --url http://localhost:8000 &
TUNNEL_PID=$!
sleep 5

# 检查是否成功
echo "=" 
echo "📊 服务状态"
echo "=" 
echo ""
echo "📍 本地访问: http://localhost:8000"
echo ""
echo "🌐 公网访问: 检查Tunnel日志中显示的地址"
echo ""
echo "🔄 Tunnel PID: $TUNNEL_PID"
echo ""
echo "💡 Tunnel地址会显示在cloudflared的输出中"
echo ""
echo "=" 
echo "🎯 提示"
echo "=" 
echo ""
echo "🔄 如果这个会话结束，Tunnel也会停止"
echo "📝 下次需要重新启动Tunnel"
echo ""
echo "="
