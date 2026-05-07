#!/bin/bash
# 历史兼容脚本：请优先使用 ./start.sh
# 兼容入口：复用标准启动脚本
set -e

cd "$(dirname "$0")/.."
exec ./start.sh
