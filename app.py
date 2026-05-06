#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资组合后端API
支持添加股票、获取实时数据、更新页面
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json
import os
import sys
from datetime import datetime

# 导入深度财务分析模块
from deep_financial_analysis import DeepFinancialAnalysis

app = Flask(__name__, static_folder='.')
CORS(app)

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 腾讯财经API接口
TENCENT_API = "http://qt.gtimg.cn/q="

# 估值参数
VALUATION_PARAMS = {
    'ideal_pe_ratio': 0.5,      # 理想PE = 历史均值 × 0.5
    'reasonable_pe_ratio': 0.7, # 合理PE = 历史均值 × 0.7
    'cautious_pe_ratio': 0.85,  # 谨慎PE = 历史均值 × 0.85
    'payout_ratio': 0.6         # 分红率（60%）
}

# 行业历史均值（供参考）
INDUSTRY_PE = {
    '白酒': 35,
    '银行': 10,
    '消费': 25,
    '科技': 40,
    '医药': 30,
    '煤炭': 12,
    '电力': 18,
    '石油': 15,
    '水务': 14,
    '其他': 20
}

@app.route('/api/get_stocks', methods=['GET'])
def get_stocks():
    """获取所有股票数据（用于前端动态渲染）"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), 'full_realtime_data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 转换为前端需要的格式
            stocks = []
            for code, info in data.items():
                # 获取实时价格
                realtime = get_realtime_data([code])
                if code in realtime:
                    r = realtime[code]
                    stock = {
                        'code': code,
                        'name': info.get('name', r.get('name', '')),
                        'currentPrice': r.get('price', 0),
                        'change': r.get('change', 0),
                        'changePercent': r.get('change_pct', r.get('changePercent', 0)),
                        'pe': r.get('pe', info.get('pe', 0)),
                        'pb': r.get('pb', info.get('pb', 0)),
                        'dividendYield': info.get('dividendYield', info.get('dividend_yield', 0)),
                        'idealBuy': info.get('idealBuy', 0),
                        'reasonableBuy': info.get('reasonableBuy', 0),
                        'cautiousBuy': info.get('cautiousBuy', 0),
                        'sector': info.get('sector', '其他'),
                        'roe': info.get('roe', 0),
                        'netMargin': info.get('netMargin', info.get('net_margin', 0)),
                        'grossMargin': info.get('grossMargin', 0.3),
                        'debtRatio': info.get('debtRatio', 0.5),
                        'high52w': info.get('high_52w', info.get('high52w', 0)),
                        'low52w': info.get('low_52w', info.get('low52w', 0)),
                    }
                    stocks.append(stock)
            
            return jsonify({'success': True, 'stocks': stocks, 'count': len(stocks)})
        else:
            return jsonify({'success': False, 'error': '数据文件不存在'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def get_realtime_data(codes):
    """
    从腾讯财经获取实时数据
    """
    results = {}
    if not codes:
        return results
    
    stock_list = [f"sh{c}" if c.startswith('6') else f"sz{c}" for c in codes]
    url = TENCENT_API + ','.join(stock_list)
    
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
                change = float(data[31]) if data[31] else 0
                change_pct = float(data[32]) if data[32] else 0
                pe = float(data[39]) if len(data) > 39 and data[39] else 0
                pb = float(data[46]) if len(data) > 46 and data[46] else 0
                roe = float(data[62])/100 if len(data) > 62 and data[62] else 0
                net_margin = float(data[64])/100 if len(data) > 64 and data[64] else 0
                high_52w = float(data[47]) if len(data) > 47 and data[47] else 0
                low_52w = float(data[48]) if len(data) > 48 and data[48] else 0
                
                dividend_yield = (VALUATION_PARAMS['payout_ratio'] / pe * 100) if pe > 0 else 0
                
                results[code] = {
                    'name': data[1],
                    'price': price,
                    'change': change,
                    'changePercent': change_pct,
                    'pe': pe,
                    'pb': pb,
                    'dividendYield': round(dividend_yield, 2),
                    'roe': roe,
                    'netMargin': net_margin,
                    'high52w': high_52w,
                    'low52w': low_52w
                }
                
    except Exception as e:
        print(f"获取实时数据失败: {e}")
    
    return results

def calculate_valuation(price, pe, industry):
    """
    计算估值买点
    """
    industry_pe = INDUSTRY_PE.get(industry, INDUSTRY_PE['其他'])
    
    ideal_buy = price * (VALUATION_PARAMS['ideal_pe_ratio'] * industry_pe / pe) if pe > 0 else price * 0.7
    reasonable_buy = price * (VALUATION_PARAMS['reasonable_pe_ratio'] * industry_pe / pe) if pe > 0 else price * 0.85
    cautious_buy = price * (VALUATION_PARAMS['cautious_pe_ratio'] * industry_pe / pe) if pe > 0 else price * 0.95
    
    return {
        'idealBuy': round(ideal_buy, 2),
        'reasonableBuy': round(reasonable_buy, 2),
        'cautiousBuy': round(cautious_buy, 2)
    }

def add_stock_to_json(stock_data, sector):
    """
    添加股票到实时数据文件
    """
    try:
        data_file = os.path.join(os.path.dirname(__file__), 'full_realtime_data.json')
        
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
        
        # 生成配置
        valuation = calculate_valuation(
            stock_data['price'],
            stock_data['pe'],
            sector
        )
        
        data[stock_data['code']] = {
            'name': stock_data['name'],
            'price': stock_data['price'],
            'change': stock_data['change'],
            'changePercent': stock_data['changePercent'],
            'pe': stock_data['pe'],
            'pb': stock_data['pb'],
            'dividendYield': stock_data['dividendYield'],
            'idealBuy': valuation['idealBuy'],
            'reasonableBuy': valuation['reasonableBuy'],
            'cautiousBuy': valuation['cautiousBuy'],
            'roe': stock_data['roe'],
            'netMargin': stock_data['netMargin'],
            'high52w': stock_data['high52w'],
            'low52w': stock_data['low52w'],
            'sector': sector
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        print(f"添加股票到文件失败: {e}")
        return False

def update_html_with_new_stock(stock_data, sector):
    """
    更新HTML文件添加新股票
    """
    try:
        html_file = os.path.join(os.path.dirname(__file__), 'index.html')
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 这里需要完整实现HTML更新逻辑
        # 暂时简化为返回成功，实际需要更新stocksConfig
        
        return True
        
    except Exception as e:
        print(f"更新HTML失败: {e}")
        return False

def search_stock_code(keyword):
    """
    根据关键词搜索股票代码（简化版）
    """
    # 常见股票映射
    stock_map = {
        '贵州茅台': '600519',
        '茅台': '600519',
        '招商银行': '600036',
        '招商': '600036',
        '中国平安': '601318',
        '平安': '601318',
        '宁德时代': '300750',
        '宁德': '300750',
        '腾讯': '00700',
        '阿里巴巴': 'BABA',
        '阿里': 'BABA'
    }
    
    # 如果是纯数字，直接返回
    if keyword.isdigit() and len(keyword) >= 5:
        return keyword
    
    # 搜索映射表
    if keyword in stock_map:
        return stock_map[keyword]
    
    # 尝试猜测（支持常见格式）
    for name, code in stock_map.items():
        if keyword in name:
            return code
    
    return None

@app.route('/')
def index():
    """首页"""
    return send_from_directory('.', 'index.html')

@app.route('/api/search', methods=['GET'])
def search_stock():
    """搜索股票"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'success': False, 'error': '请输入关键词'})
    
    code = search_stock_code(keyword)
    
    if code:
        return jsonify({'success': True, 'code': code, 'keyword': keyword})
    else:
        return jsonify({
            'success': False, 
            'error': '未找到股票，请确认股票名称或直接输入6位股票代码',
            'hint': '例如：600519（贵州茅台）'
        })

@app.route('/api/add', methods=['POST'])
def add_stock():
    """添加股票"""
    data = request.json
    keyword = data.get('keyword', '')
    sector = data.get('sector', '其他')
    
    if not keyword:
        return jsonify({'success': False, 'error': '请输入股票名称或代码'})
    
    # 搜索股票代码
    code = search_stock_code(keyword)
    if not code and len(keyword) >= 5 and keyword.isdigit():
        code = keyword
    
    if not code:
        return jsonify({'success': False, 'error': '无法确认股票代码'})
    
    # 获取实时数据
    realtime_data = get_realtime_data([code])
    if code not in realtime_data:
        return jsonify({'success': False, 'error': '无法获取股票数据'})
    
    stock_info = realtime_data[code]
    
    # 添加到数据文件
    stock_info['code'] = code
    add_stock_to_json(stock_info, sector)
    
    return jsonify({
        'success': True,
        'stock': {
            'code': code,
            'name': stock_info['name'],
            'price': stock_info['price'],
            'change': stock_info['change'],
            'changePercent': stock_info['changePercent'],
            'pe': stock_info['pe'],
            'pb': stock_info['pb'],
            'dividendYield': stock_info['dividendYield'],
            'sector': sector
        },
        'message': f'✅ {stock_info["name"]} 添加成功！'
    })

@app.route('/api/refresh', methods=['GET'])
def refresh_all():
    """刷新所有股票数据"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), 'full_realtime_data.json')
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            codes = list(data.keys())
            realtime_data = get_realtime_data(codes)
            
            for code, info in realtime_data.items():
                if code in data:
                    data[code].update(info)
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': '数据刷新成功'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/deep_analysis', methods=['GET'])
def deep_analysis():
    """深度财务分析"""
    code = request.args.get('code', '')
    if not code:
        return jsonify({'success': False, 'error': '请提供股票代码'})
    
    try:
        analyzer = DeepFinancialAnalysis()
        report = analyzer.generate_full_report(code)
        
        # 获取详细数据
        cashflow = analyzer.analyze_cashflow_quality(code)
        profit = analyzer.analyze_profit_quality(code)
        debt = analyzer.analyze_debt_risk(code)
        peers = analyzer.compare_peers(code)
        
        total_score = (cashflow.get('score', 0) + profit.get('score', 0) + debt.get('score', 0)) / 3
        
        return jsonify({
            'success': True,
            'code': code,
            'name': cashflow.get('name', ''),
            'total_score': round(total_score, 1),
            'cashflow': cashflow,
            'profit': profit,
            'debt': debt,
            'peers': peers,
            'report': report
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 投资组合API服务启动...")
    print("📱 访问: http://localhost:8002")
    print("🔧 API文档: http://localhost:8002/api/search")
    app.run(host='0.0.0.0', port=8002, debug=True)
