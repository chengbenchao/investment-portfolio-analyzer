#!/bin/bash
# 历史脚本：统一收敛到标准 tunnel 入口
set -e
cd "$(dirname "$0")"
exec ./start_tunnel.sh
