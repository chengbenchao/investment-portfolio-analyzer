#!/bin/bash
# 历史脚本：统一收敛到标准数据更新入口
set -e
cd "$(dirname "$0")"
exec ./update_data.sh
