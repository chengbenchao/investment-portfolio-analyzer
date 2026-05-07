#!/bin/bash
# 天工引擎最小一致性检查：启动链路 / 文档 / 关键文件
set -e
cd "$(dirname "$0")"

ERRORS=0
warn() { echo "⚠️  $1"; }
fail() { echo "❌ $1"; ERRORS=$((ERRORS+1)); }
ok() { echo "✅ $1"; }

echo "🔍 investment-portfolio-analyzer consistency check"

echo "\n[1] 核心文件"
for f in README.md AGENTS.md docs/architecture.md start.sh start_tunnel.sh start_public.sh selfcheck.sh update_data.sh main.py src/api/app.py src/data/fetch_real_data.py src/data/update_status.py requirements.txt smoke_test.sh deploy/investment-portfolio-analyzer.service; do
  [ -f "$f" ] && ok "$f" || fail "缺少 $f"
done

echo "\n[2] 启动脚本引用检查"
grep -q 'main.py' start.sh && ok 'start.sh 指向 main.py' || fail 'start.sh 没有指向 main.py'
grep -q '\.venv' start.sh && ok 'start.sh 使用 .venv' || warn 'start.sh 未显式使用 .venv'
if grep -q 'app.py' start.sh; then
  fail 'start.sh 仍引用不存在的 app.py'
fi

echo "\n[3] 文档一致性"
grep -q 'python3 main.py' README.md && ok 'README 使用 main.py 启动' || fail 'README 未使用 main.py 启动'
grep -q './start.sh' README.md && ok 'README 提到标准脚本 ./start.sh' || warn 'README 未提到标准脚本 ./start.sh'
grep -q '8002' README.md && ok 'README 提到端口 8002' || fail 'README 未提到端口 8002'
grep -q './start_tunnel.sh' README.md && ok 'README 提到标准 tunnel 脚本' || warn 'README 未提到标准 tunnel 脚本'
grep -q './start_public.sh' README.md && ok 'README 提到标准公网脚本' || warn 'README 未提到标准公网脚本'
grep -q 'smoke_test.sh' README.md && ok 'README 提到 smoke test' || warn 'README 未提到 smoke test'
grep -q '/healthz' README.md && ok 'README 提到 healthz' || warn 'README 未提到 healthz'
grep -q '/api/status' README.md && ok 'README 提到 /api/status' || warn 'README 未提到 /api/status'
grep -q 'update_data.sh' README.md && ok 'README 提到标准数据更新入口' || warn 'README 未提到 update_data.sh'

echo "\n[4] 运行时快速检查"
python3 - <<'PY'
import os
root='/root/.openclaw/workspace/investment-portfolio-analyzer'
assert os.path.exists(os.path.join(root,'main.py'))
assert os.path.exists(os.path.join(root,'src/api/app.py'))
print('✅ Python 路径检查通过')
PY

echo "\n[5] 兼容脚本"
grep -q 'exec ./start.sh' start_service.sh && ok 'start_service.sh 已收敛到 start.sh' || warn 'start_service.sh 未收敛'
grep -q 'exec ./start.sh' run_simple.sh && ok 'run_simple.sh 已收敛到 start.sh' || warn 'run_simple.sh 未收敛'
grep -q '127.0.0.1:8002' start_tunnel.sh && ok 'start_tunnel.sh 固定代理到 127.0.0.1:8002' || fail 'start_tunnel.sh 未固定代理到 127.0.0.1:8002'
grep -q 'exec ./start_public.sh' launch_tunnel.sh && ok 'launch_tunnel.sh 已收敛到 start_public.sh' || warn 'launch_tunnel.sh 未收敛'
grep -q 'exec ./start_public.sh' start_and_tunnel.sh && ok 'start_and_tunnel.sh 已收敛到 start_public.sh' || warn 'start_and_tunnel.sh 未收敛'
grep -q 'exec ./start_tunnel.sh' start_tunnel_and_get_url.sh && ok 'start_tunnel_and_get_url.sh 已收敛到 start_tunnel.sh' || warn 'start_tunnel_and_get_url.sh 未收敛'
grep -q '127.0.0.1:8002' smoke_test.sh && ok 'smoke_test.sh 固定测试 127.0.0.1:8002' || fail 'smoke_test.sh 未固定测试 127.0.0.1:8002'
grep -q '/healthz' smoke_test.sh && ok 'smoke_test.sh 包含 healthz' || fail 'smoke_test.sh 未包含 healthz'
grep -q 'selfcheck.sh' start.sh && ok 'start.sh 已接入启动前自检' || fail 'start.sh 未接入 selfcheck.sh'
grep -q 'logs/data_update_status.json' AGENTS.md && ok 'AGENTS.md 提到数据状态文件' || warn 'AGENTS.md 未提到数据状态文件'
grep -q 'update_data.sh' run_update_now.sh && ok 'run_update_now.sh 已收敛到 update_data.sh' || warn 'run_update_now.sh 未收敛'
grep -q 'update_data.sh' run_data_update.sh && ok 'run_data_update.sh 已收敛到 update_data.sh' || warn 'run_data_update.sh 未收敛'

echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "✅ 一致性检查通过"
else
  echo "❌ 一致性检查失败：$ERRORS 个错误"
  exit 1
fi
