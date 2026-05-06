#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股投资组合分析系统 - 主入口
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.logger import logger
from src.api.app import app

if __name__ == '__main__':
    logger.info("A股投资组合分析系统启动")
    print("=" * 70)
    print("📊 A股投资组合分析系统 v2.0")
    print("=" * 70)
    print("🚀 服务启动中...")
    print("📍 访问地址: http://localhost:8002")
    print("🔧 API文档: http://localhost:8002/api/search")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=8002, debug=True)
