#!/bin/bash
# 标准公网入口：先确保本地服务可用，再启动 tunnel
set -euo pipefail
cd "$(dirname "$0")"

LOCAL_URL="http://127.0.0.1:8002"

if curl -fsS "$LOCAL_URL/" >/dev/null 2>&1; then
  echo "✅ 本地服务已运行：$LOCAL_URL"
else
  echo "🚀 本地服务未运行，正在后台启动..."
  nohup ./start.sh > "${TMPDIR:-/tmp}/investment-portfolio-app.log" 2>&1 &
  for _ in $(seq 1 20); do
    sleep 1
    if curl -fsS "$LOCAL_URL/" >/dev/null 2>&1; then
      echo "✅ 本地服务启动成功：$LOCAL_URL"
      break
    fi
  done
fi

if ! curl -fsS "$LOCAL_URL/" >/dev/null 2>&1; then
  echo "❌ 本地服务启动失败，请先检查 ./start.sh"
  exit 1
fi

exec ./start_tunnel.sh
