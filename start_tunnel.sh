#!/bin/bash
# 标准 Tunnel 入口：仅负责把本地 8002 暴露到公网
set -euo pipefail
cd "$(dirname "$0")"

LOCAL_URL="http://127.0.0.1:8002"
TUNNEL_LOG="${TMPDIR:-/tmp}/investment-portfolio-tunnel.log"

check_local() {
  curl -fsS "$LOCAL_URL/" >/dev/null 2>&1
}

extract_url() {
  grep -Eo 'https://[a-z0-9.-]+\.trycloudflare\.com' "$TUNNEL_LOG" 2>/dev/null | head -1
}

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "❌ 未找到 cloudflared。"
  echo "请先安装 Cloudflare Tunnel 客户端，再运行 ./start_tunnel.sh"
  exit 1
fi

if ! check_local; then
  echo "❌ 本地服务未启动：$LOCAL_URL"
  echo "请先运行：./start.sh"
  exit 1
fi

echo "🧹 清理旧 tunnel 进程..."
pkill -f 'cloudflared tunnel --url http://127.0.0.1:8002' 2>/dev/null || true
rm -f "$TUNNEL_LOG"

echo "🌐 启动 Cloudflare Quick Tunnel -> $LOCAL_URL"
nohup cloudflared tunnel --url "$LOCAL_URL" > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID=$!

echo "⏳ 等待 tunnel 分配公网地址..."
URL=""
for _ in $(seq 1 20); do
  sleep 1
  URL=$(extract_url || true)
  if [ -n "$URL" ]; then
    break
  fi
  if ! kill -0 "$TUNNEL_PID" 2>/dev/null; then
    echo "❌ cloudflared 启动失败，请检查日志：$TUNNEL_LOG"
    exit 1
  fi
done

echo ""
echo "📊 Tunnel 状态"
echo "- 本地服务: $LOCAL_URL"
echo "- Tunnel PID: $TUNNEL_PID"
echo "- Tunnel 日志: $TUNNEL_LOG"
if [ -n "$URL" ]; then
  echo "- 公网地址: $URL"
  echo "✅ Tunnel 已启动"
else
  echo "⚠️  Tunnel 已启动，但暂未提取到公网地址"
  echo "   可手动查看日志：tail -f $TUNNEL_LOG"
fi
