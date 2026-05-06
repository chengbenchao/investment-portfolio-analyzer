#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股投资组合分析系统 - Flask后端API

功能：
- 实时行情获取（腾讯财经API）
- 股票搜索与添加
- 深度财务分析
- 数据刷新

作者：A股分析师
版本：2.0
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os
import sys
from datetime import datetime
from functools import wraps

# ===== 路径配置 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..', '..')
sys.path.insert(0, os.path.join(BASE_DIR, '..', 'core'))

# ===== 导入模块 =====
from utils.logger import logger
from utils.error_handler import APIError, handle_api_error

try:
    from deep_financial_analysis import DeepFinancialAnalysis
    HAS_DEEP_ANALYSIS = True
except ImportError:
    HAS_DEEP_ANALYSIS = False
    logger.warning("深度财务分析模块未加载")

# ===== Flask应用初始化 =====
app = Flask(__name__, static_folder=PROJECT_ROOT, static_url_path='/')
CORS(app)

# ===== 配置常量 =====
TENCENT_API = "https://qt.gtimg.cn/q="

DATA_FILE = os.path.join(BASE_DIR, 'full_realtime_data.json')

VALUATION_PARAMS = {
    'ideal_pe_ratio': 0.5,
    'reasonable_pe_ratio': 0.7,
    'cautious_pe_ratio': 0.85,
    'payout_ratio': 0.6
}

INDUSTRY_PE = {
    '白酒': 35, '银行': 10, '消费': 25, '科技': 40,
    '医药': 30, '煤炭': 12, '电力': 18, '石油': 15,
    '水务': 14, '其他': 20
}

# 股票名称→代码映射（支持模糊搜索）
STOCK_MAP = {
    '贵州茅台': '600519', '茅台': '600519',
    '招商银行': '600036', '招行': '600036',
    '中国平安': '601318', '平安': '601318',
    '宁德时代': '300750', '宁德': '300750',
    '比亚迪': '002594', '长江电力': '600900',
    '中国神华': '601088', '陕西煤业': '601225',
    '中国石油': '601857', '中国石化': '600028',
    '重庆水务': '601158', '工商银行': '601398',
    '建设银行': '601939', '农业银行': '601288',
    '中国银行': '601988', '交通银行': '601328',
    '邮储银行': '601658', '腾讯': '00700',
    '阿里巴巴': 'BABA', '阿里': 'BABA',
}


# ===== 工具函数 =====
def load_data():
    """加载股票数据文件"""
    if not os.path.exists(DATA_FILE):
        raise APIError('数据文件不存在，请先添加股票')
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    """保存股票数据文件"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_realtime_data(codes):
    """从腾讯财经获取实时数据"""
    results = {}
    if not codes:
        return results

    stock_list = [f"sh{c}" if c.startswith('6') else f"sz{c}" for c in codes]
    url = TENCENT_API + ','.join(stock_list)

    try:
        resp = requests.get(url, timeout=10)
        resp.encoding = 'gbk'
        resp.raise_for_status()

        for line in resp.text.strip().split(';'):
            if '~' not in line:
                continue
            line = line.split('=', 1)[-1].strip().rstrip(';').strip('"')
            data = line.split('~')
            if len(data) < 50:
                continue

            code = data[2]
            price = float(data[3]) if data[3] else 0
            pe = float(data[39]) if len(data) > 39 and data[39] else 0
            dividend_yield = round((VALUATION_PARAMS['payout_ratio'] / pe * 100), 2) if pe > 0 else 0

            results[code] = {
                'name': data[1],
                'price': price,
                'change': float(data[31]) if data[31] else 0,
                'changePercent': float(data[32]) if data[32] else 0,
                'pe': pe,
                'pb': float(data[46]) if len(data) > 46 and data[46] else 0,
                'dividendYield': dividend_yield,
                'roe': float(data[62])/100 if len(data) > 62 and data[62] else 0,
                'netMargin': float(data[64])/100 if len(data) > 64 and data[64] else 0,
                'high52w': float(data[47]) if len(data) > 47 and data[47] else 0,
                'low52w': float(data[48]) if len(data) > 48 and data[48] else 0,
            }
    except requests.RequestException as e:
        logger.error(f"腾讯API请求失败: {e}")
        raise APIError('行情数据获取失败，请稍后重试')

    return results


def calculate_valuation(price, pe, industry):
    """计算估值买点"""
    industry_pe = INDUSTRY_PE.get(industry, INDUSTRY_PE['其他'])
    if pe <= 0:
        return {'idealBuy': round(price * 0.7, 2), 'reasonableBuy': round(price * 0.85, 2), 'cautiousBuy': round(price * 0.95, 2)}

    ratio = industry_pe / pe
    return {
        'idealBuy': round(price * VALUATION_PARAMS['ideal_pe_ratio'] * ratio, 2),
        'reasonableBuy': round(price * VALUATION_PARAMS['reasonable_pe_ratio'] * ratio, 2),
        'cautiousBuy': round(price * VALUATION_PARAMS['cautious_pe_ratio'] * ratio, 2),
    }


def search_stock_code(keyword):
    """搜索股票代码"""
    if not keyword:
        return None
    if keyword.isdigit() and 5 <= len(keyword) <= 6:
        return keyword
    keyword = keyword.strip()
    if keyword in STOCK_MAP:
        return STOCK_MAP[keyword]
    for name, code in STOCK_MAP.items():
        if keyword in name:
            return code
    return None


# ===== API路由 =====

@app.route('/')
def index():
    """首页"""
    return send_from_directory(PROJECT_ROOT, 'index.html')


@app.route('/api/get_stocks', methods=['GET'])
@handle_api_error
def get_stocks():
    """获取所有股票数据"""
    data = load_data()
    codes = list(data.keys())
    realtime = get_realtime_data(codes)

    stocks = []
    for code, info in data.items():
        r = realtime.get(code, {})
        stocks.append({
            'code': code,
            'name': info.get('name', r.get('name', '')),
            'currentPrice': r.get('price', info.get('price', 0)),
            'change': r.get('change', info.get('change', 0)),
            'changePercent': r.get('changePercent', 0),
            'pe': r.get('pe', info.get('pe', 0)),
            'pb': r.get('pb', info.get('pb', 0)),
            'dividendYield': info.get('dividendYield', 0),
            'idealBuy': info.get('idealBuy', 0),
            'reasonableBuy': info.get('reasonableBuy', 0),
            'cautiousBuy': info.get('cautiousBuy', 0),
            'sector': info.get('sector', '其他'),
            'roe': info.get('roe', 0),
            'netMargin': info.get('netMargin', 0),
            'grossMargin': info.get('grossMargin', 0.3),
            'debtRatio': info.get('debtRatio', 0.5),
            'high52w': info.get('high52w', 0),
            'low52w': info.get('low52w', 0),
        })

    logger.info(f"获取股票数据成功: {len(stocks)}只")
    return jsonify({'success': True, 'stocks': stocks, 'count': len(stocks)})


@app.route('/api/search', methods=['GET'])
@handle_api_error
def search_stock():
    """搜索股票"""
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        raise APIError('请输入关键词')

    code = search_stock_code(keyword)
    if code:
        return jsonify({'success': True, 'code': code, 'keyword': keyword})
    raise APIError('未找到股票，请确认名称或输入6位代码', 404)


@app.route('/api/add', methods=['POST'])
@handle_api_error
def add_stock():
    """添加股票"""
    data = request.json
    if not data:
        raise APIError('请求体不能为空')

    keyword = data.get('keyword', '').strip()
    sector = data.get('sector', '其他').strip()
    if not keyword:
        raise APIError('请输入股票名称或代码')

    code = search_stock_code(keyword)
    if not code:
        raise APIError('无法确认股票代码')

    # 检查是否已存在
    try:
        existing = load_data()
        if code in existing:
            return jsonify({'success': False, 'error': f'{existing[code]["name"]} 已存在', 'code': code})
    except APIError:
        existing = {}

    realtime = get_realtime_data([code])
    if code not in realtime:
        raise APIError('无法获取股票数据')

    stock_info = realtime[code]
    valuation = calculate_valuation(stock_info['price'], stock_info['pe'], sector)

    existing[code] = {
        **stock_info, 'code': code, 'sector': sector,
        'idealBuy': valuation['idealBuy'],
        'reasonableBuy': valuation['reasonableBuy'],
        'cautiousBuy': valuation['cautiousBuy'],
    }
    save_data(existing)

    logger.info(f"添加股票: {code} - {stock_info['name']}")
    return jsonify({
        'success': True,
        'stock': {'code': code, 'name': stock_info['name'], 'price': stock_info['price'], 'sector': sector},
        'message': f'✅ {stock_info["name"]} 添加成功！'
    })


@app.route('/api/refresh', methods=['GET'])
@handle_api_error
def refresh_all():
    """刷新所有股票数据"""
    data = load_data()
    codes = list(data.keys())
    realtime = get_realtime_data(codes)

    for code, info in realtime.items():
        if code in data:
            data[code].update(info)
    save_data(data)

    logger.info(f"刷新数据成功: {len(codes)}只")
    return jsonify({'success': True, 'message': f'已刷新{len(codes)}只股票'})


@app.route('/api/deep_analysis', methods=['GET'])
@handle_api_error
def deep_analysis():
    """深度财务分析"""
    code = request.args.get('code', '').strip()
    if not code:
        raise APIError('请提供股票代码')

    if not HAS_DEEP_ANALYSIS:
        raise APIError('深度分析模块未加载')

    analyzer = DeepFinancialAnalysis()
    report = analyzer.generate_full_report(code)

    cashflow = analyzer.analyze_cashflow_quality(code)
    profit = analyzer.analyze_profit_quality(code)
    debt = analyzer.analyze_debt_risk(code)
    peers = analyzer.compare_peers(code)

    total_score = (cashflow.get('score', 0) + profit.get('score', 0) + debt.get('score', 0)) / 3

    logger.info(f"深度分析: {code}")
    return jsonify({
        'success': True, 'code': code,
        'name': cashflow.get('name', ''),
        'total_score': round(total_score, 1),
        'cashflow': cashflow, 'profit': profit, 'debt': debt, 'peers': peers, 'report': report
    })


# ===== 启动入口 =====
if __name__ == '__main__':
    logger.info("投资组合API服务启动")
    print("=" * 60)
    print("📊 A股投资组合分析系统 v2.0")
    print("=" * 60)
    print("🌐 访问: http://localhost:8002")
    print("📋 API: http://localhost:8002/api/get_stocks")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8002, debug=True)
