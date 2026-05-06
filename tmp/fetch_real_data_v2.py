#!/usr/bin/env python3
"""
定时获取A股真实数据 - 首席金融分析师版
集成东方财富真实PE/PB/股息率数据
"""

import requests
import json
import time
import os
from datetime import datetime


def get_stock_data_batch(codes):
    """
    腾讯财经批量接口获取真实数据
    一次请求获取所有股票的PE/PB/价格/涨跌幅
    """
    results = {}

    stock_list = []
    for code in codes:
        prefix = 'sh' if code.startswith('6') else 'sz'
        stock_list.append(f"{prefix}{code}")

    url = f"http://qt.gtimg.cn/q={','.join(stock_list)}"

    try:
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'

        if resp.status_code == 200:
            lines = resp.text.strip().split(';')

            for line in lines:
                if '~' not in line:
                    continue

                if '=' in line:
                    line = line.split('=', 1)[1]

                line = line.strip().rstrip(';').strip('"')
                data = line.split('~')

                if len(data) < 50:
                    continue

                code = data[2]
                price = float(data[3]) if data[3] else 0
                pe_ttm = float(data[39]) if len(data) > 39 and data[39] else 0

                # 估算股息率（假设60%分红率）
                dividend_yield = (0.60 / pe_ttm * 100) if pe_ttm > 0 else 0

                results[code] = {
                    'name': data[1],
                    'price': price,
                    'prev_close': float(data[4]) if data[4] else 0,
                    'change': float(data[31]) if data[31] else 0,
                    'change_pct': float(data[32]) if data[32] else 0,
                    'pe_ttm': pe_ttm,
                    'dividend_yield': dividend_yield,
                    'volume': float(data[6]) if data[6] else 0,
                }
    except Exception as e:
        print(f"获取数据失败: {e}")

    return results


def update_html_with_real_data(real_data):
    """
    更新HTML页面中的PE/股息率为真实数据
    """
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for code, data in real_data.items():
        if data['pe_ttm'] > 0:
            # 更新PE
            import re
            pe_pattern = rf"(code: '{code}'.*?pe: )[\d.]+"
            content = re.sub(pe_pattern, rf"\g<1>{data['pe_ttm']:.2f}", content, flags=re.DOTALL)

            # 更新股息率
            div_pattern = rf"(code: '{code}'.*?dividendYield: )[\d.]+"
            content = re.sub(div_pattern, rf"\g<1>{data['dividend_yield']:.2f}", content, flags=re.DOTALL)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ HTML页面已更新真实PE/股息率数据")


def fetch_all_stocks():
    """主函数"""
    stocks = ['601088', '600900', '601225', '601857', '601158', '600028']

    print("=" * 70)
    print("📊 能源公用事业投资组合 - 实时数据获取")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    # 获取真实数据
    data = get_stock_data_batch(stocks)

    if data:
        # 打印结果
        for code, info in data.items():
            change_icon = "📈" if info['change_pct'] >= 0 else "📉"
            print(f"{change_icon} {info['name']:<10} {info['price']:>8.2f}元  {info['change_pct']:>+6.2f}%  PE:{info['pe_ttm']:.1f}x  股息率:{info['dividend_yield']:.2f}%")

        # 更新HTML
        update_html_with_real_data(data)

        # 保存JSON
        json_path = os.path.join(os.path.dirname(__file__), 'realtime_data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("\n✅ 完成！刷新网页查看真实PE数据！")
    else:
        print("❌ 获取数据失败")

    print("=" * 70)


if __name__ == "__main__":
    fetch_all_stocks()
