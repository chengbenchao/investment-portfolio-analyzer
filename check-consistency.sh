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
for f in README.md AGENTS.md docs/architecture.md docs/script-governance.md start.sh start_tunnel.sh start_public.sh selfcheck.sh update_data.sh main.py index.html src/api/app.py src/data/fetch_real_data.py src/data/update_status.py requirements.txt smoke_test.sh deploy/investment-portfolio-analyzer.service legacy/start_service.sh legacy/run_simple.sh legacy/launch_tunnel.sh legacy/start_and_tunnel.sh legacy/start_tunnel_and_get_url.sh legacy/run_update_now.sh legacy/run_data_update.sh legacy/restart_stocks.sh legacy/pages/munger_index.html legacy/pages/enhanced_index.html; do
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
grep -q 'script-governance.md' README.md && ok 'README 提到脚本治理文档' || warn 'README 未提到脚本治理文档'
grep -q 'legacy/pages/' README.md && ok 'README 提到历史页面归档' || warn 'README 未提到 legacy/pages/'

echo "\n[4] 运行时快速检查"
python3 - <<'PY'
import os
root='/root/.openclaw/workspace/investment-portfolio-analyzer'
assert os.path.exists(os.path.join(root,'main.py'))
assert os.path.exists(os.path.join(root,'src/api/app.py'))
print('✅ Python 路径检查通过')
PY

echo "\n[5] 兼容脚本 / legacy 迁移"
grep -q 'exec ./start.sh' legacy/start_service.sh && ok 'legacy/start_service.sh 已收敛到 start.sh' || warn 'legacy/start_service.sh 未收敛'
grep -q 'exec ./start.sh' legacy/run_simple.sh && ok 'legacy/run_simple.sh 已收敛到 start.sh' || warn 'legacy/run_simple.sh 未收敛'
grep -q '127.0.0.1:8002' start_tunnel.sh && ok 'start_tunnel.sh 固定代理到 127.0.0.1:8002' || fail 'start_tunnel.sh 未固定代理到 127.0.0.1:8002'
grep -q 'exec ./start_public.sh' legacy/launch_tunnel.sh && ok 'legacy/launch_tunnel.sh 已收敛到 start_public.sh' || warn 'legacy/launch_tunnel.sh 未收敛'
grep -q 'exec ./start_public.sh' legacy/start_and_tunnel.sh && ok 'legacy/start_and_tunnel.sh 已收敛到 start_public.sh' || warn 'legacy/start_and_tunnel.sh 未收敛'
grep -q 'exec ./start_tunnel.sh' legacy/start_tunnel_and_get_url.sh && ok 'legacy/start_tunnel_and_get_url.sh 已收敛到 start_tunnel.sh' || warn 'legacy/start_tunnel_and_get_url.sh 未收敛'
grep -q '127.0.0.1:8002' smoke_test.sh && ok 'smoke_test.sh 固定测试 127.0.0.1:8002' || fail 'smoke_test.sh 未固定测试 127.0.0.1:8002'
grep -q '/healthz' smoke_test.sh && ok 'smoke_test.sh 包含 healthz' || fail 'smoke_test.sh 未包含 healthz'
grep -q 'selfcheck.sh' start.sh && ok 'start.sh 已接入启动前自检' || fail 'start.sh 未接入 selfcheck.sh'
grep -q 'logs/data_update_status.json' AGENTS.md && ok 'AGENTS.md 提到数据状态文件' || warn 'AGENTS.md 未提到数据状态文件'
grep -q 'legacy/pages/' AGENTS.md && ok 'AGENTS.md 提到历史页面归档目录' || warn 'AGENTS.md 未提到历史页面归档目录'
grep -q 'update_data.sh' legacy/run_update_now.sh && ok 'legacy/run_update_now.sh 已收敛到 update_data.sh' || warn 'legacy/run_update_now.sh 未收敛'
grep -q 'update_data.sh' legacy/run_data_update.sh && ok 'legacy/run_data_update.sh 已收敛到 update_data.sh' || warn 'legacy/run_data_update.sh 未收敛'
grep -q '历史兼容脚本' legacy/start_service.sh && ok '兼容脚本已标注' || warn 'legacy/start_service.sh 未标注兼容身份'
grep -q '遗留脚本' legacy/restart_stocks.sh && ok '遗留脚本已标注' || warn 'legacy/restart_stocks.sh 未标注遗留身份'

echo ""
if [ "$ERRORS" -eq 0 ]; then
  echo "✅ 一致性检查通过"
else
  echo "❌ 一致性检查失败：$ERRORS 个错误"
  exit 1
fi
