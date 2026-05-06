#!/usr/bin/env python3
"""
刷新所有A股数据 - 完整版
"""

import requests
import json
import os
from datetime import datetime


def get_stock_realtime_batch(codes):
    """腾讯财经批量获取行情+PE+PB+其他指标"""
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

                results[code] = {
                    'name': data[1],
                    'price': price,
                    'change': float(data[31]) if data[31] else 0,
                    'change_pct': float(data[32]) if data[32] else 0,
                    'pe': float(data[39]) if len(data) > 39 and data[39] else 0,
                    'pb': float(data[46]) if len(data) > 46 and data[46] else 0,
                    'roe': float(data[62])/100.0 if len(data) > 62 and data[62] else 0,
                    'net_margin': float(data[64])/100.0 if len(data) > 64 and data[64] else 0,
                    'total_market_cap': float(data[44]) if len(data) > 44 and data[44] else 0,
                    'high_52w': float(data[47]) if len(data) > 47 and data[47] else 0,
                    'low_52w': float(data[48]) if len(data) > 48 and data[48] else 0,
                }
    except Exception as e:
        print(f"行情获取失败: {e}")
    return results


def calculate_valuation(price, pe, sector):
    """计算估值买点"""
    industry_pe = {
        '煤炭': 12,
        '电力': 18,
        '石油': 15,
        '水务': 14,
        '银行': 10,
        '其他': 20
    }.get(sector, 20)
    
    ideal_pe_ratio = 0.5
    reasonable_pe_ratio = 0.7
    cautious_pe_ratio = 0.85
    
    if pe > 0:
        ideal_buy = price * (ideal_pe_ratio * industry_pe / pe)
        reasonable_buy = price * (reasonable_pe_ratio * industry_pe / pe)
        cautious_buy = price * (cautious_pe_ratio * industry_pe / pe)
    else:
        ideal_buy = price * 0.7
        reasonable_buy = price * 0.85
        cautious_buy = price * 0.95
    
    return {
        'idealBuy': round(ideal_buy, 2),
        'reasonableBuy': round(reasonable_buy, 2),
        'cautiousBuy': round(cautious_buy, 2)
    }


def main():
    # 所有股票代码和对应行业
    stocks_config = {
        '601088': {'name': '中国神华', 'sector': '煤炭', 'payout_ratio': 0.65},
        '600900': {'name': '长江电力', 'sector': '电力', 'payout_ratio': 0.70},
        '601225': {'name': '陕西煤业', 'sector': '煤炭', 'payout_ratio': 0.65},
        '601857': {'name': '中国石油', 'sector': '石油', 'payout_ratio': 0.45},
        '601158': {'name': '重庆水务', 'sector': '水务', 'payout_ratio': 0.60},
        '600028': {'name': '中国石化', 'sector': '石油', 'payout_ratio': 0.50},
        '600036': {'name': '招商银行', 'sector': '银行', 'payout_ratio': 0.60},
    }
    
    codes = list(stocks_config.keys())
    
    print("=" * 70)
    print("📊 A股数据自动更新 - 首席金融分析师")
    print(f"🕐 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    print("🔍 获取实时行情数据...")
    realtime = get_stock_realtime_batch(codes)
    
    print("\n" + "=" * 70)
    print("📊 数据汇总")
    print("=" * 70)
    
    all_data = {}
    for code in codes:
        config = stocks_config[code]
        rt = realtime.get(code, {})
        
        # 计算股息率
        pe = rt.get('pe', 0)
        dividend_yield = (config['payout_ratio'] / pe * 100) if pe > 0 else 0
        
        # 计算估值
        valuation = calculate_valuation(
            rt.get('price', 0),
            pe,
            config['sector']
        )
        
        all_data[code] = {
            'name': rt.get('name', config['name']),
            'price': rt.get('price', 0),
            'change': rt.get('change', 0),
            'change_pct': rt.get('change_pct', 0),
            'changePercent': rt.get('change_pct', 0),  # 兼容两种格式
            'pe': pe,
            'pb': rt.get('pb', 0),
            'dividend_yield': round(dividend_yield, 2),
            'dividendYield': round(dividend_yield, 2),  # 兼容两种格式
            'roe': rt.get('roe', 0),
            'net_margin': rt.get('net_margin', 0),
            'netMargin': rt.get('net_margin', 0),  # 兼容两种格式
            'total_market_cap': rt.get('total_market_cap', 0),
            'high_52w': rt.get('high_52w', 0),
            'high52w': rt.get('high_52w', 0),  # 兼容两种格式
            'low_52w': rt.get('low_52w', 0),
            'low52w': rt.get('low_52w', 0),  # 兼容两种格式
            'sector': config['sector'],
            'idealBuy': valuation['idealBuy'],
            'reasonableBuy': valuation['reasonableBuy'],
            'cautiousBuy': valuation['cautiousBuy'],
        }
    
    # 打印结果
    for code, info in all_data.items():
        change_icon = "📈" if info['change_pct'] >= 0 else "📉"
        print(f"\n{change_icon} {info['name']} ({code})")
        print(f"   价格: {info['price']:.2f}元  涨跌幅: {info['change_pct']:+.2f}%")
        print(f"   PE: {info['pe']:.2f}x  PB: {info['pb']:.2f}x  股息率: {info['dividend_yield']:.2f}%")
        print(f"   买点: 理想{info['idealBuy']:.2f}  合理{info['reasonableBuy']:.2f}  谨慎{info['cautiousBuy']:.2f}")
    
    # 保存到正确的位置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    save_path = os.path.join(project_root, 'src', 'data', 'full_realtime_data.json')
    
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print(f"✅ 数据已保存至: {save_path}")
    print("=" * 70)
    
    return all_data


if __name__ == "__main__":
    main()
