#!/bin/bash
# 自动启动A股投资组合并获取Cloudflare Tunnel地址

echo "=" 
echo "🚀 启动A股投资组合服务"
echo "=" 

# 停止旧的进程
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
echo "🚀 启动HTTP服务器（8000端口）..."
python3 -m http.server 8000 &
sleep 2

# 启动Cloudflare Tunnel
echo ""
echo "🌐 启动Cloudflare Tunnel..."
echo "⏳ 请稍等，正在连接..."
echo ""

# 在后台启动Tunnel，保存输出到临时文件
cloudflared tunnel --url http://localhost:8000 > /tmp/tunnel_output.txt 2>&1 &
TUNNEL_PID=$!
sleep 5

# 检查Tunnel是否成功
echo ""
echo "=" 
echo "📊 服务状态"
echo "=" 
echo ""
echo "📍 本地访问: http://localhost:8000"
echo ""

# 尝试从输出文件中提取地址
if [ -f /tmp/tunnel_output.txt ]; then
    TUNNEL_URL=$(grep -Eo 'https://[a-z0-9.-]+\.trycloudflare\.com' /tmp/tunnel_output.txt | head -1)
    
    if [ -n "$TUNNEL_URL" ]; then
        echo "🌐 公网访问: $TUNNEL_URL"
        echo ""
        echo "✅ 完成！"
        echo ""
        echo "💡 提示：如果Tunnel断开，请重新运行此脚本"
        echo ""
        echo "=" 
        echo "🎯 Tunnel进程信息"
        echo "=" 
        echo "   Tunnel PID: $TUNNEL_PID"
        echo "   输出文件: /tmp/tunnel_output.txt"
        echo ""
        echo "=" 
        echo "⚠️  重要提示"
        echo "=" 
        echo "   每次重启Tunnel，地址都会变化"
        echo "   Tunnel需要保持运行才能访问"
        echo ""
    else
        echo "🔄 Tunnel正在启动中，可能需要更长时间..."
        echo ""
        echo "💡 可以尝试查看Tunnel输出："
        echo "   tail -f /tmp/tunnel_output.txt"
        echo ""
    fi
else
    echo "❌ Tunnel输出文件不存在，请检查..."
    echo ""
fi

echo "=" 

# 保持脚本运行，不退出
echo ""
echo "💡 服务已启动！"
echo ""
echo "💡 如果需要停止，按Ctrl+C，然后手动停止Tunnel进程"
echo ""

# 保持脚本运行
sleep 3600
