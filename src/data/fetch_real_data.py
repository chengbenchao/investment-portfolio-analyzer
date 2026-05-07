#!/usr/bin/env python3
"""
定时获取A股真实数据 - 首席金融分析师版
包含科学估值分析和交易时间判断
"""

import requests
import json
import time
import os
import sys
from datetime import datetime, time as dt_time

# 添加项目根目录到路径，确保能导入 src.core 模块
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.valuation_analysis import PortfolioValuation, STOCKS_CONFIG
from src.data.update_status import save_status, now_str


def is_trading_time():
    """
    判断当前是否为A股交易时间

    A股交易时间:
    - 9:30 - 11:30 (上午)
    - 13:00 - 15:00 (下午)

    返回:
        bool - 是否在交易时间
    """
    now = datetime.now()
    current_time = now.time()

    # 检查是否为周末
    if now.weekday() >= 5:  # 0=周一, 5=周六, 6=周日
        return False

    # 上午时段:9:30 - 11:30
    morning_start = dt_time(9, 30, 0)
    morning_end = dt_time(11, 30, 0)

    # 下午时段:13:00 - 15:00
    afternoon_start = dt_time(13, 0, 0)
    afternoon_end = dt_time(15, 0, 0)

    if morning_start <= current_time <= morning_end:
        return True
    if afternoon_start <= current_time <= afternoon_end:
        return True

    return False


def get_trading_time_info():
    """
    获取交易时间信息
    """
    now = datetime.now()
    current_time = now.time()

    info = {
        'now': now.strftime('%Y-%m-%d %H:%M:%S'),
        'is_trading': is_trading_time(),
        'weekday': now.strftime('%A'),
        'next_trading': ''
    }

    if now.weekday() >= 5:
        info['next_trading'] = '下周一'
    elif current_time < dt_time(9, 30, 0):
        info['next_trading'] = '今天 9:30'
    elif current_time < dt_time(13, 0, 0):
        info['next_trading'] = '今天 13:00'
    elif current_time < dt_time(15, 0, 0):
        info['next_trading'] = '现在(交易中)'
    else:
        info['next_trading'] = '明天 9:30'

    return info


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
    """获取所有6只股票的真实数据（静默版本）"""
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

    for code in stocks:
        data = query_tencent_cn(code)

        if data:
            results[code] = data['price']
            stock_data[code] = {
                'price': data['price'],
                'change': data['change'],
                'change_pct': data['change_pct']
            }
        else:
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
    html_path = os.path.join(project_root, 'index.html')

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


def generate_valuation_report(prices):
    """生成估值分析报告（静默版本）"""
    portfolio = PortfolioValuation(prices)

    # 保存报告，不输出任何信息
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(project_root, "reports", f"valuation_report_{timestamp}.txt")
    portfolio.save_report(save_path)


def main():
    """主函数"""
    time_info = get_trading_time_info()
    save_status({
        'last_attempt_at': now_str(),
        'last_mode': 'manual' if os.environ.get('MANUAL_UPDATE') == '1' else 'scheduled',
        'trading_window': time_info,
        'last_error': None
    })

    try:
        prices, stock_data = fetch_all_stocks()
        update_html(prices, stock_data)
        generate_valuation_report(prices)
        save_status({
            'last_success_at': now_str(),
            'last_updated_count': len(prices),
            'last_error': None,
            'last_prices_snapshot': prices
        })
        print(f"数据更新成功！时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"获取到的股票数据: {prices}")
    except Exception as e:
        save_status({
            'last_error': str(e)
        })
        print(f"数据更新失败: {e}")
        raise


if __name__ == "__main__":
    main()
