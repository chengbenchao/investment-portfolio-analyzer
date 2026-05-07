#!/bin/bash
# 历史脚本：保持兼容，统一走标准入口
set -e
cd "$(dirname "$0")"
exec ./start.sh
