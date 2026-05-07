#!/bin/bash
# 最小 smoke test：验证首页和关键 API 是否可访问
set -euo pipefail
cd "$(dirname "$0")"

BASE_URL="http://127.0.0.1:8002"

ok() { echo "✅ $1"; }
fail() { echo "❌ $1"; exit 1; }

fetch() {
  curl -fsS "$1"
}

echo "🧪 smoke test: $BASE_URL"

# 1. 首页
fetch "$BASE_URL/" >/dev/null && ok "首页可访问 /" || fail "首页不可访问 /"
fetch "$BASE_URL/classic" >/dev/null && ok "经典页可访问 /classic" || fail "经典页不可访问 /classic"

# 2. 健康检查
HEALTH_JSON=$(fetch "$BASE_URL/healthz") || fail "/healthz 不可访问"
printf '%s' "$HEALTH_JSON" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"ok"' && ok "/healthz 返回 ok" || fail "/healthz 未返回 ok"

# 3. 数据状态 API
STATUS_JSON=$(fetch "$BASE_URL/api/status") || fail "/api/status 不可访问"
printf '%s' "$STATUS_JSON" | grep -q 'success' && ok "/api/status 返回 success" || fail "/api/status 未返回 success"

# 4. 搜索 API（使用代码，避免中文 URL/别名差异）
SEARCH_JSON=$(fetch "$BASE_URL/api/search?keyword=600519") || fail "/api/search 不可访问"
printf '%s' "$SEARCH_JSON" | grep -q 'success' && ok "/api/search 返回 success" || fail "/api/search 未返回 success"

# 5. 芒格偏差 API
BIAS_JSON=$(fetch "$BASE_URL/api/munger/biases") || fail "/api/munger/biases 不可访问"
printf '%s' "$BIAS_JSON" | grep -q 'success' && ok "/api/munger/biases 返回 success" || fail "/api/munger/biases 未返回 success"

# 6. 投资组合 API
STOCK_JSON=$(fetch "$BASE_URL/api/get_stocks") || fail "/api/get_stocks 不可访问"
printf '%s' "$STOCK_JSON" | grep -q 'success' && ok "/api/get_stocks 返回 success" || fail "/api/get_stocks 未返回 success"

echo "✅ smoke test 通过"
