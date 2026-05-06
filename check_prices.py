#!/usr/bin/env python3
"""
查询6只股票的当前价格并判断买入时机
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入股票查询函数
import requests
import time


def get_stock_price_tencent(code):
    """从腾讯财经获取股票价格"""
    try:
        if code.startswith('6'):
            url = f"http://qt.gtimg.cn/q=sh{code}"
        else:
            url = f"http://qt.gtimg.cn/q=sz{code}"
        
        response = requests.get(url, timeout=5)
        response.encoding = 'gbk'
        text = response.text
        
        if 'v_pv_none_match' in text:
            return None
        
        data = text.split('~')
        if len(data) < 45:
            return None
        
        name = data[1]
        price = float(data[3])
        prev_close = float(data[4])
        change = price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
        
        return {
            'code': code,
            'name': name,
            'price': price,
            'prev_close': prev_close,
            'change': change,
            'change_percent': change_percent
        }
    except Exception as e:
        print(f"查询 {code} 失败: {e}")
        return None


def main():
    """查询6只股票并判断买入时机"""
    stocks = [
        {'code': '601088', 'name': '中国神华', 'ideal': 30, 'reasonable': 33, 'cautious': 36},
        {'code': '600900', 'name': '长江电力', 'ideal': 24, 'reasonable': 27, 'cautious': 30},
        {'code': '601225', 'name': '陕西煤业', 'ideal': 17, 'reasonable': 20, 'cautious': 23},
        {'code': '601857', 'name': '中国石油', 'ideal': 8, 'reasonable': 9, 'cautious': 10},
        {'code': '601158', 'name': '重庆水务', 'ideal': 6, 'reasonable': 7, 'cautious': 8},
        {'code': '600028', 'name': '中国石化', 'ideal': 6, 'reasonable': 7, 'cautious': 8}
    ]
    
    print("\n" + "="*80)
    print("📊 6只股票当前价格查询 (2026-05-06)")
    print("="*80)
    
    print(f"\n{'股票名称':<10} {'代码':<8} {'当前价格':>10} {'涨跌幅':>10} {'理想买点':>10} {'合理买点':>10} {'判断':<15}")
    print("-"*80)
    
    results = []
    
    for stock in stocks:
        data = get_stock_price_tencent(stock['code'])
        if data:
            price = data['price']
            change_pct = data['change_percent']
            
            # 判断买入时机
            if price <= stock['ideal']:
                signal = "🟢 理想买点"
            elif price <= stock['reasonable']:
                signal = "🟡 合理买点"
            elif price <= stock['cautious']:
                signal = "🟠 谨慎买点"
            else:
                signal = "🔴 建议观望"
            
            print(f"{stock['name']:<10} {stock['code']:<8} {price:>10.2f} {change_pct:>+9.2f}% {stock['ideal']:>10} {stock['reasonable']:>10} {signal:<15}")
            
            results.append({
                'code': stock['code'],
                'name': stock['name'],
                'price': price,
                'change_percent': change_pct,
                'signal': signal
            })
        else:
            print(f"{stock['name']:<10} {stock['code']:<8} {'--':>10} {'--':>10} {stock['ideal']:>10} {stock['reasonable']:>10} {'查询失败':<15}")
        
        time.sleep(0.5)
    
    print("\n" + "="*80)
    print("\n💡 建议:")
    print("  🟢 = 理想买点，建议买入")
    print("  🟡 = 合理买点，可以买入")
    print("  🟠 = 谨慎买点，少量配置")
    print("  🔴 = 价格偏高，建议观望")
    print("\n" + "="*80)
    
    return results


if __name__ == '__main__':
    main()
