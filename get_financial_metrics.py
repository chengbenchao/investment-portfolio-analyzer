#!/usr/bin/env python3
"""
获取真实财务指标 - 使用东方财富财务指标接口
"""

import requests
import json


def get_financial_metrics_v2(codes):
    """
    使用东方财富财务指标接口获取ROE、毛利率、净利率等
    """
    results = {}
    for code in codes:
        secid = f"1.{code}" if code.startswith('6') else f"0.{code}"
        
        # 使用财务指标接口
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f173,f174,f175,f176,f177,f178,f179,f180,f181,f182"
        
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://quote.eastmoney.com'
        }
        
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('data'):
                    d = data['data']
                    # f173=ROE, f174=毛利率, f175=净利率, f176=资产负债率
                    roe_raw = d.get('f173', 0)
                    gross_raw = d.get('f174', 0)
                    net_raw = d.get('f175', 0)
                    debt_raw = d.get('f176', 0)
                    
                    # 这些字段可能是百分比形式（如18.5表示18.5%）
                    # 也可能是原始值，需要判断
                    results[code] = {
                        'roe': float(roe_raw) / 100.0 if roe_raw and float(roe_raw) > 1 else float(roe_raw) if roe_raw else 0,
                        'gross_margin': float(gross_raw) / 100.0 if gross_raw and float(gross_raw) > 1 else float(gross_raw) if gross_raw else 0,
                        'net_margin': float(net_raw) / 100.0 if net_raw and float(net_raw) > 1 else float(net_raw) if net_raw else 0,
                        'debt_ratio': float(debt_raw) / 100.0 if debt_raw and float(debt_raw) > 1 else float(debt_raw) if debt_raw else 0,
                    }
                    print(f"{code}: ROE原始={roe_raw}, 毛利率原始={gross_raw}, 净利率原始={net_raw}")
        except Exception as e:
            print(f"获取 {code} 财务数据失败: {e}")
        
    return results


def get_dividend_history(codes):
    """
    获取历史分红数据计算真实股息率
    """
    results = {}
    for code in codes:
        secid = f"1.{code}" if code.startswith('6') else f"0.{code}"
        
        # 获取分红送配数据
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f188"
        
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('data'):
                    # f188是股息率(%)
                    dy = data['data'].get('f188', 0)
                    if dy:
                        results[code] = float(dy)
        except:
            pass
    
    return results


def main():
    codes = ['601088', '600900', '601225', '601857', '601158', '600028']
    
    print("🔍 获取财务指标...")
    financials = get_financial_metrics_v2(codes)
    
    print("\n🔍 获取股息率...")
    dividends = get_dividend_history(codes)
    
    print("\n" + "=" * 70)
    print("📊 财务数据汇总")
    print("=" * 70)
    
    for code in codes:
        fin = financials.get(code, {})
        div = dividends.get(code, 0)
        print(f"\n{code}:")
        print(f"  ROE: {fin.get('roe', 0)*100:.1f}%")
        print(f"  毛利率: {fin.get('gross_margin', 0)*100:.1f}%")
        print(f"  净利率: {fin.get('net_margin', 0)*100:.1f}%")
        print(f"  资产负债率: {fin.get('debt_ratio', 0)*100:.1f}%")
        print(f"  股息率: {div:.2f}%")
    
    # 保存
    all_data = {code: {**financials.get(code, {}), 'dividend_yield': dividends.get(code, 0)} for code in codes}
    with open('investment-portfolio/financial_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 已保存至 financial_metrics.json")


if __name__ == "__main__":
    main()
