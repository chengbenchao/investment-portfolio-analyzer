#!/bin/bash
# 标准数据更新入口
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="python3"
if [ -x ".venv/bin/python" ]; then
  VENV_PY="$(pwd)/.venv/bin/python"
  if "$VENV_PY" -c "import requests" >/dev/null 2>&1; then
    PYTHON="$VENV_PY"
  fi
fi

echo "📊 开始执行数据更新..."
MANUAL_UPDATE=1 exec "$PYTHON" src/data/fetch_real_data.py
