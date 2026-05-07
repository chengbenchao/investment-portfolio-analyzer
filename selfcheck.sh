#!/bin/bash
# 启动前自检：依赖、入口、端口
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="python3"
if [ -x ".venv/bin/python" ]; then
  VENV_PY="$(pwd)/.venv/bin/python"
  if "$VENV_PY" -c "import flask, flask_cors, requests" >/dev/null 2>&1; then
    PYTHON="$VENV_PY"
  fi
fi

ok() { echo "✅ $1"; }
fail() { echo "❌ $1"; exit 1; }

[ -f main.py ] && ok "main.py 存在" || fail "缺少 main.py"
[ -f src/api/app.py ] && ok "src/api/app.py 存在" || fail "缺少 src/api/app.py"

"$PYTHON" -c "import flask, flask_cors, requests" >/dev/null 2>&1 \
  && ok "Python 依赖可导入（当前使用: $PYTHON）" \
  || fail "缺少 Python 依赖，请先执行: python3 -m pip install -r requirements.txt"

if ss -ltn '( sport = :8002 )' | grep -q 8002; then
  ok "端口 8002 已被监听（若是本项目实例，可直接访问）"
else
  ok "端口 8002 当前空闲，可启动服务"
fi
