#!/usr/bin/env python3
"""
获取完整真实数据并更新网页
"""

import requests
import json


def get_all_realtime_data(codes):
    """腾讯财经批量获取所有数据"""
    results = {}
    stock_list = [f"sh{c}" if c.startswith('6') else f"sz{c}" for c in codes]
    url = f"http://qt.gtimg.cn/q={','.join(stock_list)}"
    
    try:
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'
        
        if resp.status_code == 200:
            for line in resp.text.strip().split(';'):
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
                
                # 真实财务数据
                roe = float(data[62]) / 100.0 if len(data) > 62 and data[62] else 0
                net_margin = float(data[64]) / 100.0 if len(data) > 64 and data[64] else 0
                
                # 股息率估算（基于真实PE和合理分红率）
                pe = float(data[39]) if len(data) > 39 and data[39] else 0
                payout_ratios = {'601088':0.65,'600900':0.70,'601225':0.65,'601857':0.45,'601158':0.60,'600028':0.50}
                ratio = payout_ratios.get(code, 0.5)
                dividend_yield = (ratio / pe * 100) if pe > 0 else 0
                
                results[code] = {
                    'name': data[1],
                    'price': price,
                    'change': float(data[31]) if data[31] else 0,
                    'change_pct': float(data[32]) if data[32] else 0,
                    'pe': pe,
                    'pb': float(data[46]) if len(data) > 46 and data[46] else 0,
                    'roe': roe,
                    'net_margin': net_margin,
                    'dividend_yield': round(dividend_yield, 2),
                    'total_market_cap': float(data[44]) if len(data) > 44 and data[44] else 0,
                    'high_52w': float(data[47]) if len(data) > 47 and data[47] else 0,
                    'low_52w': float(data[48]) if len(data) > 48 and data[48] else 0,
                }
    except Exception as e:
        print(f"获取失败: {e}")
    
    return results


def main():
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']
    
    print("🔍 获取完整真实数据...")
    data = get_all_realtime_data(codes)
    
    print("\n" + "=" * 70)
    print("📊 完整真实数据汇总")
    print("=" * 70)
    
    for code, info in data.items():
        print(f"\n📌 {info['name']} ({code})")
        print(f"   PE: {info['pe']:.2f}x  PB: {info['pb']:.2f}x")
        print(f"   ROE: {info['roe']*100:.1f}%  净利率: {info['net_margin']*100:.1f}%")
        print(f"   股息率: {info['dividend_yield']:.2f}%")
        print(f"   52周高/低: {info['high_52w']:.2f} / {info['low_52w']:.2f}")
    
    # 保存
    with open('investment-portfolio/full_realtime_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 已保存至 full_realtime_data.json")
    print("=" * 70)
    
    return data


if __name__ == "__main__":
    main()
