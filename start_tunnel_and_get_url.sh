#!/bin/bash
# 启动A股投资组合和Cloudflare Tunnel

cd /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio

# 清理旧进程
pkill -f "cloudflare" 2>/dev/null
pkill -f "python3.*http.server" 2>/dev/null
pkill -f "python.*investment" 2>/dev/null
sleep 2

# 启动Python HTTP服务器
echo "🚀 启动A股投资组合（8000端口）..."
python3 -m http.server 8000 &
sleep 2

# 启动Cloudflare Tunnel
echo "🌐 启动Cloudflare Tunnel..."
echo "⏳ 请稍等，Tunnel正在连接..."

# 启动tunnel并获取输出
cloudflared tunnel --url http://localhost:8000 > /tmp/tunnel_output.txt 2>&1 &
TUNNEL_PID=$!

# 等待几秒让tunnel启动
sleep 8

# 检查是否有输出
echo ""
echo "=" 
echo "📊 服务状态"
echo "=" 
echo ""
echo "📍 本地访问: http://localhost:8000"
echo ""

# 尝试从输出中提取地址
if [ -f /tmp/tunnel_output.txt ]; then
    TUNNEL_URL=$(grep -Eo 'https://[a-z0-9.-]+\.trycloudflare\.com' /tmp/tunnel_output.txt | head -1)
    
    if [ -n "$TUNNEL_URL" ]; then
        echo "🌐 公网访问: $TUNNEL_URL"
        echo ""
        echo "✅ Tunnel已启动成功！"
    else
        echo "🔄 Tunnel正在启动，URL会自动显示在cloudflared输出中"
        echo ""
        echo "💡 你也可以手动运行此命令查看："
        echo "   cat /tmp/tunnel_output.txt"
    fi
fi

echo ""
echo "=" 
echo "🎯 提示"
echo "=" 
echo ""
echo "🔄 这个会话结束，Tunnel也会停止"
echo "📝 下次需要重新启动Tunnel"
echo ""
echo "="
