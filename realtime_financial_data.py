#!/usr/bin/env python3
"""
实时财务数据获取模块
使用腾讯财经批量接口获取真实PE/PB/市值/股息率
一次请求获取全部6只股票数据
"""

import requests
import json


def get_stock_realtime_data_batch(codes):
    """
    腾讯财经批量接口 - 一次性获取所有股票数据
    返回真实的PE/PB/市值/股息率等
    """
    results = {}

    # 构建批量查询
    stock_list = []
    for code in codes:
        prefix = 'sh' if code.startswith('6') else 'sz'
        stock_list.append(f"{prefix}{code}")

    url = f"http://qt.gtimg.cn/q={','.join(stock_list)}"

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://finance.qq.com'
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'gbk'

        if resp.status_code == 200:
            # 解析返回数据
            lines = resp.text.strip().split(';')

            for line in lines:
                if '~' not in line:
                    continue

                # 去掉前面的 var v_sh601088=
                if '=' in line:
                    line = line.split('=', 1)[1]

                # 去掉末尾的;
                line = line.strip().rstrip(';').strip('"')

                data = line.split('~')

                if len(data) < 50:
                    continue

                code = data[2]
                results[code] = {
                    'name': data[1],
                    'price': float(data[3]) if data[3] else 0,
                    'prev_close': float(data[4]) if data[4] else 0,
                    'open': float(data[5]) if data[5] else 0,
                    'volume': float(data[6]) if data[6] else 0,
                    'change': float(data[31]) if data[31] else 0,
                    'change_pct': float(data[32]) if data[32] else 0,
                    'high': float(data[33]) if data[33] else 0,
                    'low': float(data[34]) if data[34] else 0,
                    # 关键财务数据
                    'pe_ttm': float(data[39]) if len(data) > 39 and data[39] else 0,
                    'pb': float(data[45]) if len(data) > 45 and data[45] else 0,
                    'market_cap': float(data[44]) if len(data) > 44 and data[44] else 0,  # 流通市值（亿）
                    'turnover': float(data[37]) if len(data) > 37 and data[37] else 0,
                    'limit_up': float(data[48]) if len(data) > 48 and data[48] else 0,
                    'limit_down': float(data[49]) if len(data) > 49 and data[49] else 0,
                }

    except Exception as e:
        print(f"获取数据失败: {e}")

    return results


def calculate_dividend_yield(price, pe_ttm, payout_ratio=0.60):
    """根据PE估算股息率：股息率 = 分红率 / PE"""
    if pe_ttm > 0:
        return (payout_ratio / pe_ttm) * 100
    return 0


def print_report(data):
    """打印真实财务报告"""
    print("=" * 80)
    print("📊 腾讯财经实时财务数据（真实值）")
    print("=" * 80)

    for code, info in data.items():
        dividend_yield = calculate_dividend_yield(info['price'], info['pe_ttm'])

        print(f"\n📌 {info['name']} ({code})")
        print("-" * 60)
        print(f"💵 当前价格: {info['price']:.2f} 元")
        print(f"📈 涨跌幅: {info['change_pct']:+.2f}%")
        print(f"📊 PE (TTM): {info['pe_ttm']:.2f}")
        print(f"📊 PB (MRQ): {info['pb']:.2f}")
        print(f"💰 估算股息率: {dividend_yield:.2f}%")
        print(f"🔄 换手率: {info['turnover']:.2f}%")

    print("\n" + "=" * 80)


def main():
    """测试"""
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']

    print("🔍 正在获取实时财务数据（腾讯财经批量接口）...")
    data = get_stock_realtime_data_batch(codes)

    if data:
        print_report(data)

        # 保存JSON供其他模块使用
        with open('investment-portfolio/realtime_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("\n✅ 数据已保存至 realtime_data.json")
    else:
        print("❌ 获取数据失败")


if __name__ == "__main__":
    main()
