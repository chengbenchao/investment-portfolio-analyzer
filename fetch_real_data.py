#!/usr/bin/env python3
"""
定时获取A股真实数据 - 首席金融分析师版
包含科学估值分析
"""

import requests
import json
import time
import os
from datetime import datetime
from valuation_analysis import PortfolioValuation, STOCKS_CONFIG


def detect_prefix(code):
    """识别股票代码前缀"""
    if code.startswith('6'):
        return 'sh'
    elif code.startswith(('0', '3')):
        return 'sz'
    else:
        return 'sh'


def parse_tencent_response(text):
    """解析腾讯财经响应"""
    try:
        data = text.split('~')
        if len(data) < 45:
            return None

        return {
            'name': data[1],
            'code': data[2],
            'price': float(data[3]),
            'change': float(data[31]),
            'change_pct': float(data[32]),
        }
    except Exception:
        return None


def query_tencent_cn(code):
    """通过腾讯财经查询A股"""
    prefix = detect_prefix(code)
    url = f"http://qt.gtimg.cn/q={prefix}{code}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            result = parse_tencent_response(resp.text)
            if result:
                return result
    except Exception:
        pass
    return None


def fetch_all_stocks():
    """获取所有6只股票的真实数据"""
    stocks = [
        '601088',
        '600900',
        '601225',
        '601857',
        '601158',
        '600028',
    ]

    results = {}
    stock_data = {}

    print("=" * 70)
    print("📊 能源公用事业投资组合 - 首席金融分析师")
    print(f"🕐 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    for code in stocks:
        print(f"🔍 查询 {STOCKS_CONFIG.get(code, {}).get('name', code)} ({code})...", end='', flush=True)

        data = query_tencent_cn(code)

        if data:
            results[code] = data['price']
            stock_data[code] = {
                'price': data['price'],
                'change': data['change'],
                'change_pct': data['change_pct']
            }
            change_class = "📈" if data['change'] >= 0 else "📉"
            print(f" {change_class} {data['price']:.2f} ({data['change']:+.2f}, {data['change_pct']:+.2f}%)")
        else:
            print(" ❌ 获取失败，使用参考价格")
            # 使用默认参考价格
            if code == '601088':
                results[code] = 47.42
                stock_data[code] = {'price': 47.42, 'change': 0, 'change_pct': 0}
            elif code == '600900':
                results[code] = 27.11
                stock_data[code] = {'price': 27.11, 'change': 0, 'change_pct': 0}
            elif code == '601225':
                results[code] = 25.39
                stock_data[code] = {'price': 25.39, 'change': 0, 'change_pct': 0}
            elif code == '601857':
                results[code] = 11.93
                stock_data[code] = {'price': 11.93, 'change': 0, 'change_pct': 0}
            elif code == '601158':
                results[code] = 4.44
                stock_data[code] = {'price': 4.44, 'change': 0, 'change_pct': 0}
            elif code == '600028':
                results[code] = 5.35
                stock_data[code] = {'price': 5.35, 'change': 0, 'change_pct': 0}

        time.sleep(0.3)

    return results, stock_data


def update_html(prices, stock_data):
    """更新HTML页面数据"""
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建估值分析
    portfolio = PortfolioValuation(prices)
    analyses = []

    for code in STOCKS_CONFIG.keys():
        if code in prices:
            advice = portfolio.analyses[code].generate_advice()
            analyses.append((code, advice))

    # 构建新的JavaScript配置
    js_config = []
    for code, advice in analyses:
        # 获取真实的涨跌数据
        if code in stock_data:
            change = stock_data[code]['change']
            change_pct = stock_data[code]['change_pct']
        else:
            change = 0
            change_pct = 0

        entry = f"""{{
            code: '{code}',
            name: '{advice['name']}',
            sector: '{STOCKS_CONFIG[code]['sector']}',
            currentPrice: {advice['current_price']},
            change: {change},
            changePercent: {change_pct},
            pe: {advice['metrics']['pe']:.2f},
            pb: {advice['metrics']['pb']:.2f},
            dividendYield: {advice['metrics']['dividend_yield']:.2f},
            idealBuy: {advice['ideal']},
            reasonableBuy: {advice['reasonable']},
            cautiousBuy: {advice['cautious']}
        }}"""
        js_config.append(entry)

    js_config_str = "const stocksConfig = [\n        " + ",\n        ".join(js_config) + "\n    ];"

    # 替换原来的配置
    import re
    content = re.sub(
        r"const stocksConfig = \[[\s\S]*?\];",
        js_config_str,
        content
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ HTML页面已更新: {html_path}")


def generate_valuation_report(prices):
    """生成估值分析报告"""
    portfolio = PortfolioValuation(prices)

    # 生成报告
    report = portfolio.generate_full_report()
    print("\n" + report)

    # 保存报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(os.path.dirname(__file__), f"valuation_report_{timestamp}.txt")
    portfolio.save_report(save_path)
    print(f"\n📝 详细报告已保存: {save_path}")


def main():
    """主函数"""
    prices, stock_data = fetch_all_stocks()
    update_html(prices, stock_data)
    generate_valuation_report(prices)

    print("\n" + "=" * 70)
    print("🎉 完成！刷新网页即可查看最新分析")
    print("=" * 70)


if __name__ == "__main__":
    main()
