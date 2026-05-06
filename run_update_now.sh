#!/bin/bash
# A股数据立即更新脚本
cd /root/.openclaw/.arkclaw-team/agents/a-mojhmp2nzoh09g/workspace/investment-portfolio
source venv/bin/activate
python src/data/fetch_real_data.py
