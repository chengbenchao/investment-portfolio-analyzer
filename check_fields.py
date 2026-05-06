#!/usr/bin/env python3
"""
腾讯财经批量接口 - 获取所有可用字段
"""

import requests
import json

codes = ['601088', '600900', '601225', '601857', '601158', '600028']
stock_list = [f"sh{c}" if c.startswith('6') else f"sz{c}" for c in codes]
url = f"http://qt.gtimg.cn/q={','.join(stock_list)}"

resp = requests.get(url, timeout=10)
resp.encoding = 'gbk'

# 打印所有字段
for line in resp.text.strip().split(';')[:1]:  # 只看第一只股票
    if '~' not in line:
        continue
    if '=' in line:
        line = line.split('=', 1)[1]
    line = line.strip().rstrip(';').strip('"')
    data = line.split('~')
    
    print(f"股票: {data[1]} ({data[2]})")
    print(f"价格: {data[3]}")
    print(f"昨收: {data[4]}")
    print(f"开盘: {data[5]}")
    print(f"成交量: {data[6]}")
    print(f"外盘: {data[7]}")
    print(f"内盘: {data[8]}")
    # ... 继续打印关键字段
    print(f"\n[30-60] 关键财务字段:")
    for i in range(30, min(60, len(data))):
        print(f"  f{i}: {data[i]}")
    
    print(f"\n[60-100] 更多字段:")
    for i in range(60, min(100, len(data))):
        print(f"  f{i}: {data[i]}")
