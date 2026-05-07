#!/bin/bash

# 启动A股投资组合分析系统

cd /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio

# 激活虚拟环境
source venv/bin/activate

# 启动服务
echo "🚀 启动A股投资组合分析系统..."
echo "🌐 访问地址: http://localhost:8002"
echo ""

python src/api/app.py
